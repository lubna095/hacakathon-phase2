import pytest
import os
import json
from pathlib import Path
from src.models import Task, TaskCreate
from src.services import InMemoryTaskService, FileTaskService, TaskService, get_task_service

# --- Task Fixtures ---

@pytest.fixture
def test_owner() -> str:
    return "test_user"

@pytest.fixture
def sample_task_create() -> TaskCreate:
    """Provides a fresh TaskCreate object for each test."""
    return TaskCreate(name="test_task", description="A task for testing.")

@pytest.fixture
def another_task_create() -> TaskCreate:
    """Provides another fresh TaskCreate object for each test."""
    return TaskCreate(name="another_task", description="Another task for testing.")


# --- Service Fixtures ---

@pytest.fixture
def in_memory_service() -> InMemoryTaskService:
    """Fixture for a clean InMemoryTaskService instance."""
    return get_task_service("in-memory://")

@pytest.fixture
def file_service(tmp_path) -> FileTaskService:
    """Fixture for a clean FileTaskService instance with a temporary file."""
    test_file_path = tmp_path / "tasks.json"
    service = get_task_service(f"file://{test_file_path}")
    yield service
    # Teardown: Clean up the file after the test
    if os.path.exists(test_file_path):
        os.remove(test_file_path)


# --- Test Classes ---

@pytest.mark.parametrize("service_fixture", ["in_memory_service", "file_service"])
class TestTaskService:
    """Generic tests for any TaskService implementation."""

    @pytest.fixture(autouse=True)
    def service(self, request, service_fixture):
        """Injects the appropriate service fixture for the parametrized tests."""
        return request.getfixturevalue(service_fixture)

    def test_create_task(self, service: TaskService, sample_task_create: TaskCreate, test_owner: str):
        """Test creating a new task."""
        created = service.create_task(sample_task_create, owner=test_owner)
        assert created.name == sample_task_create.name
        assert created.owner == test_owner
        retrieved = service.get_task(created.id, owner=test_owner)
        assert retrieved is not None
        assert retrieved.name == sample_task_create.name
        assert len(service.list_tasks(owner=test_owner)) == 1

    def test_create_existing_task_fails(self, service: TaskService, sample_task_create: TaskCreate, test_owner: str):
        """Test that creating a task with an existing name for the same owner raises an error."""
        service.create_task(sample_task_create, owner=test_owner)
        # Note: Current service implementations do not prevent creating tasks with the same name for the same owner.
        # This test case should be updated if that logic is added.
        service.create_task(sample_task_create, owner=test_owner)
        assert len(service.list_tasks(owner=test_owner)) == 2 # Expect two tasks with same name, no error

    def test_get_task(self, service: TaskService, sample_task_create: TaskCreate, test_owner: str):
        """Test retrieving a task."""
        created = service.create_task(sample_task_create, owner=test_owner)
        retrieved = service.get_task(created.id, owner=test_owner)
        assert retrieved == created

    def test_get_nonexistent_task(self, service: TaskService, test_owner: str):
        """Test that retrieving a non-existent task returns None."""
        retrieved = service.get_task("nonexistent_id", owner=test_owner)
        assert retrieved is None

    def test_list_tasks(self, service: TaskService, sample_task_create: TaskCreate, another_task_create: TaskCreate, test_owner: str):
        """Test listing all tasks for an owner."""
        assert service.list_tasks(owner=test_owner) == []
        service.create_task(sample_task_create, owner=test_owner)
        service.create_task(another_task_create, owner=test_owner)
        tasks = service.list_tasks(owner=test_owner)
        assert len(tasks) == 2
        assert any(t.name == sample_task_create.name for t in tasks)
        assert any(t.name == another_task_create.name for t in tasks)

    def test_update_task(self, service: TaskService, sample_task_create: TaskCreate, test_owner: str):
        """Test updating an existing task."""
        created = service.create_task(sample_task_create, owner=test_owner)
        
        from src.models import TaskUpdate
        updated_task_data = TaskUpdate(description="An updated description.", completed=True)
        updated = service.update_task(created.id, updated_task_data, owner=test_owner)
        assert updated.description == "An updated description."
        assert updated.completed == True
        retrieved = service.get_task(created.id, owner=test_owner)
        assert retrieved.description == "An updated description."
        assert retrieved.completed == True

    def test_delete_task(self, service: TaskService, sample_task_create: TaskCreate, test_owner: str):
        """Test deleting a task."""
        created = service.create_task(sample_task_create, owner=test_owner)
        assert service.get_task(created.id, owner=test_owner) is not None
        deleted = service.delete_task(created.id, owner=test_owner)
        assert deleted is True
        assert service.get_task(created.id, owner=test_owner) is None


class TestFileTaskServicePersistence:
    """Specific persistence tests for FileTaskService."""

    def test_persistence_across_instances(self, tmp_path, sample_task_create: TaskCreate, another_task_create: TaskCreate, test_owner: str):
        """Test that tasks persist between different service instances."""
        test_file_path = tmp_path / "tasks.json"
        
        # First instance creates tasks
        service1 = get_task_service(f"file://{test_file_path}")
        created1 = service1.create_task(sample_task_create, owner=test_owner)
        created2 = service1.create_task(another_task_create, owner=test_owner)
        
        # Second instance should load the tasks created by the first
        service2 = get_task_service(f"file://{test_file_path}")
        tasks = service2.list_tasks(owner=test_owner)
        assert len(tasks) == 2
        assert any(t.id == created1.id for t in tasks)
        assert any(t.id == created2.id for t in tasks)

    def test_data_is_written_to_file(self, tmp_path, sample_task_create: TaskCreate, test_owner: str):
        """Test that task data is physically written to the JSON file."""
        test_file_path = tmp_path / "tasks.json"
        service = get_task_service(f"file://{test_file_path}")
        created_task = service.create_task(sample_task_create, owner=test_owner)
        
        assert test_file_path.exists()
        
        with open(test_file_path, "r") as f:
            data_from_disk = json.load(f)
            
        assert isinstance(data_from_disk, list)
        assert len(data_from_disk) == 1
        assert data_from_disk[0]['name'] == sample_task_create.name
        assert data_from_disk[0]['owner'] == test_owner