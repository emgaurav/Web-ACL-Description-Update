import boto3
import botocore
import json
import sys

def get_profiles():
    session = boto3.Session()
    return session.available_profiles

def get_web_acls(session, region, scope):
    try:
        wafv2 = session.client('wafv2', region_name=region)
        response = wafv2.list_web_acls(Scope=scope)
        return response['WebACLs']
    except botocore.exceptions.ClientError as e:
        print(f"Error: Unable to fetch WebACLs from {region}. {e}")
        return []

def update_web_acl_description(session, web_acl, new_description, region, scope):
    wafv2 = session.client('wafv2', region_name=region)
    
    try:
        current_acl = wafv2.get_web_acl(
            Name=web_acl['Name'],
            Scope=scope,
            Id=web_acl['Id']
        )

        update_params = {
            'Name': web_acl['Name'],
            'Scope': scope,
            'Id': web_acl['Id'],
            'DefaultAction': current_acl['WebACL']['DefaultAction'],
            'Description': new_description,
            'Rules': current_acl['WebACL']['Rules'],
            'VisibilityConfig': current_acl['WebACL']['VisibilityConfig'],
            'LockToken': current_acl['LockToken']
        }

        if 'CustomResponseBodies' in current_acl['WebACL']:
            update_params['CustomResponseBodies'] = current_acl['WebACL']['CustomResponseBodies']
        if 'CaptchaConfig' in current_acl['WebACL']:
            update_params['CaptchaConfig'] = current_acl['WebACL']['CaptchaConfig']
        if 'TokenDomains' in current_acl['WebACL']:
            update_params['TokenDomains'] = current_acl['WebACL']['TokenDomains']

        response = wafv2.update_web_acl(**update_params)
        print(f"Successfully updated description for WebACL: {web_acl['Name']} in {region}")
    except botocore.exceptions.ClientError as e:
        print(f"Error updating WebACL: {e}")

def main():
    profiles = get_profiles()
    print("Available profiles:")
    for i, profile in enumerate(profiles, 1):
        print(f"{i}. {profile}")
    profile_index = int(input("Select a profile (enter the number): ")) - 1
    selected_profile = profiles[profile_index]

    try:
        session = boto3.Session(profile_name=selected_profile)
        
        print("\nAvailable regions:")
        print("1. Global (CloudFront)")
        print("2. ap-south-1")
        region_choice = int(input("Select a region (enter the number): "))
        
        if region_choice == 1:
            region = 'us-east-1'
            scope = 'CLOUDFRONT'
            print("\nFetching CloudFront (global) WebACLs...")
        elif region_choice == 2:
            region = 'ap-south-1'
            scope = 'REGIONAL'
            print("\nFetching ap-south-1 regional WebACLs...")
        else:
            print("Invalid choice. Exiting.")
            sys.exit(1)
        
        web_acls = get_web_acls(session, region, scope)
        
        if not web_acls:
            print(f"No WebACLs found in the {region} region.")
            sys.exit(0)
        
        print("\nAvailable WebACLs:")
        for i, acl in enumerate(web_acls, 1):
            print(f"{i}. {acl['Name']}")
        
        acl_index = int(input("Select a WebACL (enter the number): ")) - 1
        selected_acl = web_acls[acl_index]

        new_description = input("\nEnter the new description for the WebACL: ")

        update_web_acl_description(session, selected_acl, new_description, region, scope)
    
    except botocore.exceptions.ProfileNotFound:
        print(f"Error: The selected profile '{selected_profile}' was not found.")
        print("Please ensure the profile is correctly configured in your AWS credentials file.")
    except botocore.exceptions.NoCredentialsError:
        print(f"Error: No credentials found for the selected profile '{selected_profile}'.")
        print("Please ensure your AWS credentials are properly configured for this profile.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()
