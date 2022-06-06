use aws_config::meta::region::RegionProviderChain;
use aws_sdk_ec2::output::DescribeInstancesOutput;
use aws_sdk_ec2::{Client as Ec2Client, Error as Ec2Error};
use aws_sdk_iam::output::ListRolesOutput;
use aws_sdk_iam::{Client as IamClient, Error};

use clap::{Args, Parser, Subcommand};

#[derive(Debug, Parser)]
#[clap(name = "scipio")]
#[clap(about = "AWS reconnaissance tool.", long_about = None)]
struct Scopio {
    #[clap(subcommand)]
    command: Commands,
}

#[derive(Debug, Subcommand)]
enum Commands {
    Iam(Iam),
    Ec2(Ec2),
}

#[derive(Debug, Args)]
#[clap(args_conflicts_with_subcommands = true)]
struct Iam {
    #[clap(subcommand)]
    command: Option<IamCommands>,

    #[clap(flatten)]
    list_admins: IamListAdmins,
}

#[derive(Debug, Args)]
#[clap(args_conflicts_with_subcommands = true)]
struct Ec2 {
    #[clap(subcommand)]
    command: Option<Ec2Commands>,

    #[clap(flatten)]
    describe_ec2: Ec2Describe,
}

#[derive(Debug, Subcommand)]
enum Ec2Commands {
    DescribeInstances(Ec2Describe),
}

#[derive(Debug, Subcommand)]
enum IamCommands {
    ListAdmins(IamListAdmins),
}

#[derive(Debug, Args)]
struct Ec2Describe {
    #[clap(short, long)]
    message: Option<String>,
}

#[derive(Debug, Args)]
struct IamListAdmins {
    #[clap(short, long)]
    message: Option<String>,
}

#[tokio::main]
async fn describe_all_instances() -> Result<DescribeInstancesOutput, Ec2Error> {
    let region_provider = RegionProviderChain::default_provider().or_else("us-east-1");
    let config = aws_config::from_env().region(region_provider).load().await;
    let client = Ec2Client::new(&config);

    let resp = client.describe_instances().send().await?;

    Ok(resp)
}

#[tokio::main]
async fn list_all_roles() -> Result<ListRolesOutput, Error> {
    let region_provider = RegionProviderChain::default_provider().or_else("us-east-1");
    let config = aws_config::from_env().region(region_provider).load().await;
    let client = IamClient::new(&config);

    let resp = client.list_roles().send().await?;

    Ok(resp)
}

fn display_roles(list_roles: ListRolesOutput) {
    println!("IAM Roles:");

    let roles = list_roles.roles().unwrap_or_default();

    for role in roles {
        match role.role_name.clone() {
            Some(found_role) => println!("{}", found_role),
            None => println!("No role name."),
        }
    }

    println!();
    println!("Found {} roles", roles.len());
}
fn display_instances(describe_instances: DescribeInstancesOutput) {
    println!("{:?}", describe_instances);
    println!("Ec2 Instances:");

    let instances = describe_instances.reservations;

    match instances {
        Some(found_instances) => println!("{:?}", found_instances),
        None => println!("No instances found."),
    }
}

fn main() {
    let args = Scopio::parse();

    match args.command {
        Commands::Ec2(ec2) => {
            let ec2_cmd = ec2
                .command
                .unwrap_or(Ec2Commands::DescribeInstances(ec2.describe_ec2));
            match ec2_cmd {
                Ec2Commands::DescribeInstances(_describe_ec2) => match describe_all_instances() {
                    Ok(instances_described) => display_instances(instances_described),
                    Err(e) => println!("{:?}", e),
                },
            }
        }

        Commands::Iam(iam) => {
            let iam_cmd = iam
                .command
                .unwrap_or(IamCommands::ListAdmins(iam.list_admins));
            match iam_cmd {
                IamCommands::ListAdmins(_list_admins) => match list_all_roles() {
                    Ok(list_roles) => display_roles(list_roles),
                    Err(e) => println!("{:?}", e),
                },
            }
        }
    }
}
