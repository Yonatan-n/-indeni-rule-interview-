import json
from os import stat
from typing import List

from cloudrail.entities.ec2 import Ec2


def load_instances(cloud_json_data) -> List[Ec2]:
    # TODO: Part 1.a -  given a json object, parse it to a list of ec2
    ec2s = []
    for inst in cloud_json_data['Instances']:
        instance_id = inst['InstanceId']
        name =  inst['PrivateDnsName']
        network_interfaces_ids = inst.get('NetworkInterfaces', []) 
        state =  inst['State']['Name']
        image_id =  inst['ImageId']
        availability_zone =  inst['Placement'].get('AvailabilityZone', None)
        tags =  { _json["Key"] : _json["Value"] for _json  in inst['Tags']}
        ec2s.append(Ec2(instance_id,name,network_interfaces_ids,state,image_id,availability_zone,tags))
    return ec2s


def get_ec2_contains_production_tag(ec2s: List[Ec2]) -> List[Ec2]:
    # TODO: Part 1.b - find all ec2s that have tag environment=production
    return [ec2 for ec2 in ec2s if ec2.tags.get('environment',None) == "production"]

def main():
    cloud_json_data_file = 'cloudrail/cloud-data/ec2-describe-instances.json'
    with open(cloud_json_data_file, 'r') as json_file:
        cloud_json_data = json.load(json_file)

    ec2s: List[Ec2] = load_instances(cloud_json_data)

    ec2s_with_issue = get_ec2_contains_production_tag(ec2s)
    print('Found {} ec2s with issues'.format(len(ec2s_with_issue)))


if __name__ == '__main__':
    main()
