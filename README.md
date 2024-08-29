# AWS WAF WebACL Description Updater

This Python script allows you to update the description of AWS WAF WebACLs in either the Global (CloudFront) region or the ap-south-1 region. It provides a simple command-line interface to select your AWS profile, choose a region, select a WebACL, and update its description. It comes handy for one of those cases when you forget updating description while ACL creation and AWS won't allow you to add description via console.

## Prerequisites

- Python 3.6 or higher
- Boto3 library
- Configured AWS CLI with appropriate profiles and permissions

## Installation

1. Clone this repository or download the script.
2. Install the required Python library: `pip install boto3`

## Usage

1. Run the script: `python waf_description_updater.py`
2. Follow the prompts:
- Select an AWS profile
- Choose a region (Global for CloudFront or ap-south-1)
- Select a WebACL from the list
- Enter a new description for the selected WebACL

## Features

- Supports multiple AWS profiles
- Allows updating WebACLs in both Global (CloudFront) and ap-south-1 regions
- Fetches and displays available WebACLs for the selected region
- Updates only the description of the selected WebACL, preserving all other settings

## Security Note

This script does not store or transmit any AWS credentials. It relies on your local AWS CLI configuration for authentication.

## Caution

Always ensure you have the necessary permissions and understand the implications of modifying AWS WAF WebACLs before using this script.



