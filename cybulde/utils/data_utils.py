from pathlib import Path

from cybulde.utils.utils import get_logger, run_shell_command



DATA_UTILS_LOGGER = get_logger(Path(__file__).name)

def is_dvc_initialized() -> bool:
    return (Path().cwd() / ".dvc").exists()

def initialize_dvc() -> None:
    if is_dvc_initialized():
        DATA_UTILS_LOGGER.info("DVC is already initialized")
        return

    DATA_UTILS_LOGGER.info("Initializing DVC")
    run_shell_command("dvc init")
    run_shell_command("dvc config core.analytics false")
    run_shell_command("dvc config core.autostage true")
    run_shell_command("git add .dvc")
    run_shell_command("git commit -nm 'Initialized DVC'")

def is_dvc_storage_initialized():
    return run_shell_command("dvc remote list")


def initialize_dvc_storage(dvc_remote_name: str, dvc_remote_url: str) -> None:

    if is_dvc_storage_initialized():
        DATA_UTILS_LOGGER.info(f"DVC storage {dvc_remote_name} is already initialized")
        return
    
    DATA_UTILS_LOGGER.info(f"Initialing DVC storage {dvc_remote_name}")
    run_shell_command(f"dvc remote add -d -f {dvc_remote_name} {dvc_remote_url}")
    run_shell_command(f"dvc push -r {dvc_remote_name}")
    run_shell_command("git add .dvc/config")
    run_shell_command(f"git commit -nm 'Initilized DVC storage {dvc_remote_name}'")

def commit_to_dvc(dvc_raw_data_folder: str, dvc_remote_name: str) -> None:
    current_version  = ""
    if not current_version:
        current_version = "0"
    next_version = f"v{int(current_version)+1}"

    DATA_UTILS_LOGGER.info("Commiting to DVC")
    run_shell_command(f"dvc add {dvc_raw_data_folder}")
    run_shell_command(f"git add .")
    run_shell_command(f"git commit -nm 'Updated version of the data from v{current_version} to {next_version}'")
    run_shell_command(f"git tag -a {next_version} -m 'Data version {next_version}'")
    run_shell_command(f"dvc push {dvc_raw_data_folder}.dvc --remote {dvc_remote_name}")
    run_shell_command("git push --follow-tags")
    run_shell_command("git push -f --tags")



def make_new_data_version(dvc_raw_data_folder: str, dvc_remote_name: str) -> None:
    try:
        status = run_shell_command(f"dvc status {dvc_raw_data_folder}.dvc")
        if status == "Data and pipelines are up to date.\n":
            DATA_UTILS_LOGGER.info("Data and pipelines are up to date")
            return
        commit_to_dvc(dvc_raw_data_folder, dvc_remote_name)

    except:
        commit_to_dvc(dvc_raw_data_folder, dvc_remote_name)


