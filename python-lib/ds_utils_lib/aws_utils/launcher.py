import os
import boto3
from typing import List, Dict, Any


class StackLauncher:
    """
    Class to launch and manage CloudFormation stacks.
    """

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
        bucket = os.getenv("ASSETS_BUCKET_NAME")
        template_key = f"aws-stacks/{self.stack_name}.yml"
        validation = cf.validate_template(
            TemplateURL=f"https://s3.amazonaws.com/{bucket}/{template_key}"
        )

        return validation["Parameters"]

    def validate_stack_parameters(self, parameter_set: Dict):
        """
        Check that the parameters given for the template are valid and that
        all necessary parameters are provided.
        """
        pass

    def launch(self, **kwargs):
        """
        Creates the stack from the template.
        :param kwargs: Parameters for the stack in dictionary with
            parameterName -> parameterValue mapping.
        :return:
        """
        pass
