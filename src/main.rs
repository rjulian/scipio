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

fn display_roles(list_roles: ListRolesOutput, mut writer: impl std::io::Write) {
    if let Err(e) = writeln!(writer, "IAM Roles:") {
        println!("{:?}", e)
    };

    let roles = list_roles.roles().unwrap_or_default();

    for role in roles {
        match role.role_name.clone() {
            Some(found_role) => {
                if let Err(e) = writeln!(writer, "{}", found_role) {
                    println!("{:?}", e)
                }
            }
            None => {
                if let Err(e) = writeln!(writer, "No role name.") {
                    println!("{:?}", e)
                }
            }
        };
    }

    if let Err(e) = writeln!(writer) {
        println!("{:?}", e)
    };
    if let Err(e) = writeln!(writer, "Found {} roles", roles.len()) {
        println!("{:?}", e)
    };
}
fn display_instances(describe_instances: DescribeInstancesOutput, mut writer: impl std::io::Write) {
    if let Err(e) = writeln!(writer, "{:?}", describe_instances) {
        println!("{:?}", e)
    };
    if let Err(e) = writeln!(writer, "Ec2 Instances:") {
        println!("{:?}", e)
    };

    let instances = describe_instances.reservations;

    match instances {
        Some(found_instances) => {
            if let Err(e) = writeln!(writer, "{:?}", found_instances) {
                println!("{:?}", e)
            }
        }
        None => {
            if let Err(e) = writeln!(writer, "No instances found.") {
                println!("{:?}", e)
            }
        }
    };
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
                    Ok(instances_described) => {
                        display_instances(instances_described, &mut std::io::stdout())
                    }
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
                    Ok(list_roles) => display_roles(list_roles, &mut std::io::stdout()),
                    Err(e) => println!("{:?}", e),
                },
            }
        }
    }
}
