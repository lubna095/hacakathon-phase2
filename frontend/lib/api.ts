import axios from 'axios';

export const api = axios.create({
  baseURL: 'http://localhost:8000',
});

export interface Task {
  id: string;
  name: string;
  description: string;
  completed: boolean;
  owner: string;
}

export async function getAllTasks(): Promise<Task[]> {
  const response = await api.get('/tasks');
  return response.data;
}

export async function addTask(name: string, description: string): Promise<Task> {
  const response = await api.post('/tasks', { name, description });
  return response.data;
}

export async function updateTask(id: string, name: string, description: string, completed: boolean): Promise<Task> {
  const response = await api.put(`/tasks/${id}`, { name, description, completed });
  return response.data;
}

export async function deleteTask(id: string): Promise<void> {
  await api.delete(`/tasks/${id}`);
}
