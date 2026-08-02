from custom_nodes.shared.utils import get_logger, run_command

logger = get_logger("test")
output = run_command(["python", "--version"], logger)
print(output)