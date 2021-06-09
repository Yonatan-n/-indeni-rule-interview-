from typing import Dict, List
import re
from cloudrail.knowledge.context.environment_context import EnvironmentContext
from cloudrail.knowledge.rules.aws.aws_base_rule import AwsBaseRule
from cloudrail.knowledge.rules.base_rule import Issue
from cloudrail.knowledge.rules.rule_parameters.base_paramerter import ParameterType


class EnsureThereAreNoEc2WithSimilarNamesRule(AwsBaseRule):
    def execute(self, env_context: EnvironmentContext, parameters: Dict[ParameterType, any]) -> List[Issue]:
        def is_name_similar(name1: str, name2: str) -> bool:
            index = 0
            flag = False
            while index < min(len(name1), len(name2)):
                if name1[index] != name2[index]:
                    flag = True
                    break
                index += 1
            # 1 letter diff or less
            if flag == False and max(len(name1), len(name2)) - index <= 1:
                return True
            if name1[index+1:] == name2[index:] or name1[index:] == name2[index+1:] or name1[index+1:] == name2[index+1:]:
                return True
            return False

        issues: List[Issue] = []
        # TODO: Part 3 - using cloudrail-knowledge package write rule logic that alerts (creates an issue)
        # if the 2 ec2 instances contain similar name. See readme.md for similarity definition
        for index, ec2 in enumerate(env_context.ec2s):
            rest_of_ec2s = env_context.ec2s[:index] + \
                env_context.ec2s[index+1:]
            print(ec2.name, [x.name for x in rest_of_ec2s])
            for other_ec2 in rest_of_ec2s:
                if not is_name_similar(ec2.name, other_ec2.name):
                    issues.append(Issue(
                        f"{ec2.name} is similar to {other_ec2.name}",
                        ec2,
                        other_ec2))
        # skip every second item, becase issues are inserted twice
        return issues[::2]

    def get_id(self) -> str:
        return 'ensure_there_are_no_ec2_with_similar_names_rule'

    def should_run_rule(self, environment_context: EnvironmentContext) -> bool:
        return True
