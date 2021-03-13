import os
import boto3
from ..constants import META_DIR
from typing import List, Dict, Any
from ..load_env import load_env_vars

# Load lib env variables
load_env_vars()


class StackLauncher:
    """
    Class to launch and manage CloudFormation stacks.
    """

    #: Name of assets bucket parameter in templates
    ASSETS_BUCKET_PARAM: str = "AssetsBucketName"

    #: Name of metadata file (in ~/.ds-utils-data)
    META_FILE: str = os.path.join(META_DIR, "stacks-metadata.json")

    def __init__(
            self,
            stack_name: str,
            aws_profile: str = "default",
            aws_region: str = "us-west-2"):
        """

        :param stack_name: Name of the stack.
        :param aws_profile: Name of AWS profile to select credentials.
        """
        self.__stack_name = stack_name
        self.__aws_profile = aws_profile
        self.__aws_region = aws_region
        self.__boto3_session = boto3.Session(
            profile_name=aws_profile,
            region_name=aws_region
        )

    @property
    def stack_name(self) -> str:
        """
        Read-only name of the stack.
        """
        return self.__stack_name

    @property
    def aws_region(self) -> str:
        """
        Read-only name of the region the stack will be deployed to.
        """
        return self.__aws_region

    @property
    def boto3_session(self) -> boto3.Session:
        """
        Read-only boto3 session.
        """
        return self.__boto3_session

    @property
    def template_url(self) -> str:
        """
        Read-only S3 URL of the template.
        """
        bucket = os.getenv("ASSETS_BUCKET_NAME")
        template_key = f"aws-stacks/{self.stack_name}.yml"
        return f"https://s3.amazonaws.com/{bucket}/{template_key}"

    def get_cloudformation_client(self):
        """
        Gets a cloudFormation client from the current session.
        :return: CloudFormation boto3 client.
        """
        return self.boto3_session.client("cloudformation")

    def reset_session(self, aws_profile: str, aws_region: str = "us-west-2"):
        """
        Set a new boto3 session.
        :param aws_profile: Name of aws profile for credentials.
        :param aws_region: Name of aws region.
        """
        self.__boto3_session = boto3.Session(
            profile_name=aws_profile,
            region_name=aws_region
        )

    def get_stack_parameters(self) -> List[Dict[str, Any]]:
        """
        Get the list of parameters required by the stack.
        :return: List of parameters given by boto3 API.
        """
        cf = self.get_cloudformation_client()

        # Validate the template from S3
        validation = cf.validate_template(TemplateURL=self.template_url)
        return validation["Parameters"]

    def validate_stack_parameters(
            self,
            parameter_set: Dict[str, Any]) -> bool:
        """
        Check that the parameters given for the template are valid and that
        all necessary parameters are provided.
        :param parameter_set: ParameterKey -> ParameterValue dictionary.
        :return: True if the parameter set includes the assets bucket key,
            False otherwise. Raises exception if parameters are not valid.
        """
        out = False
        valid_params = set()
        required_params = set()
        template_params = self.get_stack_parameters()

        # Get sets of valid and required parameters
        for p in template_params:
            key = p.get("ParameterKey")
            valid_params.add(key)

            if key == self.ASSETS_BUCKET_PARAM:
                out = True
            elif "DefaultValue" not in p:
                required_params.add(key)

        # Check given parameters
        for k in parameter_set.keys():
            if k not in valid_params:
                raise KeyError(f"Unknown parameter given: {k}")
            if k in required_params:
                required_params.remove(k)

        # Check that all required params were given
        if len(required_params) > 0:
            raise ValueError(
                "Required parameters not given: %s"
                % (", ".join(required_params))
            )
        return out

    def launch(self, **kwargs):
        """
        Creates the stack from the template.
        :param kwargs: Parameters for the stack in dictionary with
            parameterName -> parameterValue mapping.
        :return: StackID.
        """
        include_bucket = self.validate_stack_parameters(kwargs)
        if include_bucket:
            kwargs.update({
                self.ASSETS_BUCKET_PARAM: os.getenv("ASSETS_BUCKET_NAME")
            })

        # Create list of parameters in CloudFormation Expected Format
        parameters_list = []
        for key, val in kwargs.items():
            parameters_list.append({
                "ParameterKey": key,
                "ParameterValue": val
            })

        cf = self.get_cloudformation_client()
        result = cf.create_stack(
            StackName=self.stack_name,
            Parameters=parameters_list,
            TemplateURL=self.template_url,
            Capabilities=["CAPABILITY_NAMED_IAM"]
        )
        return result

    def delete_stack(self):
        """
        Deletes the stack.
        """
        cf = self.get_cloudformation_client()
        cf.delete_stack(StackName=self.stack_name)
