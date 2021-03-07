import boto3
from typing import List, Dict, Any


class StackLauncher:
    """
    Class to launch and manage CloudFormation stacks.
    """

    def __init__(self, stack_name: str):
        """

        :param stack_name: Name of the stack.
        """
        self.__stack_name = stack_name

    def get_stack_parameters(self) -> List[Dict[str, Any]]:
        """
        Get the list of parameters required by the stack.
        :return: List of parameters given by boto3 API.
        """
        pass

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
