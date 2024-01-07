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

def is_dvc_storage_initialized(dvc_remote_name):
    return not run_shell_command("dvc remote list")


def initialize_dvc_storage(dvc_remote_name: str, dvc_remote_url: str) -> None:

    if is_dvc_storage_initialized(dvc_remote_name):
        DATA_UTILS_LOGGER.info(f"DVC storage {dvc_remote_name} is already initialized")
        return
    
    DATA_UTILS_LOGGER.info(f"Initialing DVC storage {dvc_remote_name}")
    run_shell_command(f"dvc remote add -d -f {dvc_remote_name} {dvc_remote_url}")
    run_shell_command(f"dvc push -r {dvc_remote_name}")
    run_shell_command("git add .dvc/config")
    run_shell_command(f"git commit -nm 'Initilized DVC storage {dvc_remote_name}'")