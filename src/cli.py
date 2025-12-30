import click
from src.models import Task
from src.services import get_task_service

@click.group(invoke_without_command=True)
@click.pass_context
def cli(ctx):
    """A simple CLI to manage tasks."""
    task_service = ctx.obj
    if ctx.invoked_subcommand is None:
        main_loop(task_service)

def main_loop(task_service):
    try:
        # task_service is now passed directly
        click.echo(f"Using storage: {task_service.file_path}")
    except ValueError as e:
        click.echo(f"Error initializing storage: {e}", err=True)
        return

    while True:
        click.echo("\n--- Task Management CLI ---")
        click.echo("1. Add a new task")
        click.echo("2. View all tasks")
        click.echo("3. Update a task")
        click.echo("4. Delete a task")
        click.echo("5. Toggle task completion")
        click.echo("6. Exit")
        choice = click.prompt("Enter your choice", type=int)

        if choice == 1:
            name = click.prompt("Enter task name").strip('"')
            description = click.prompt("Enter task description").strip('"')
            try:
                task = Task(name=name, description=description)
                created_task = task_service.create_task(task)
                click.echo(f"Task '{created_task.name}' created successfully.")
            except ValueError as e:
                click.echo(f"Error: {e}", err=True)
        elif choice == 2:
            tasks = task_service.list_tasks()
            if not tasks:
                click.echo("No tasks found.")
                continue
            click.echo("\n--- All Tasks ---")
            for task in tasks:
                status = "✓" if task.completed else " "
                click.echo(f"[{status}] {task.name}: {task.description}")
        elif choice == 3:
            name = click.prompt("Enter the name of the task to update").strip('"')
            current_task = task_service.get_task(name)
            if not current_task:
                click.echo(f"Task '{name}' not found.", err=True)
                continue
            
            new_name = click.prompt(f"Enter new name (current: {current_task.name})", default=current_task.name).strip('"')
            new_description = click.prompt(f"Enter new description (current: {current_task.description})", default=current_task.description).strip('"')
            
            task_update = Task(name=new_name, description=new_description, completed=current_task.completed)

            try:
                updated = task_service.update_task(name, task_update)
                if updated:
                    click.echo(f"Task '{name}' updated successfully.")
                else:
                    click.echo(f"Failed to update task '{name}'.", err=True)
            except ValueError as e:
                click.echo(f"Error: {e}", err=True)

        elif choice == 4:
            name = click.prompt("Enter the name of the task to delete").strip('"')
            if task_service.delete_task(name):
                click.echo(f"Task '{name}' deleted successfully.")
            else:
                click.echo(f"Task '{name}' not found.", err=True)
        elif choice == 5:
            name = click.prompt("Enter the name of the task to toggle completion").strip('"')
            task = task_service.toggle_task_completion(name)
            if task:
                status = "completed" if task.completed else "not completed"
                click.echo(f"Task '{task.name}' marked as {status}.")
            else:
                click.echo(f"Task '{name}' not found.", err=True)
        elif choice == 6:
            click.echo("Exiting Task Management CLI. Goodbye!")
            break
        else:
            click.echo("Invalid choice. Please try again.")

if __name__ == '__main__':
    cli()
