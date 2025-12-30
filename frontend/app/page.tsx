'use client';

import { useState, useEffect, useCallback } from 'react';
import { useAuth } from '@/context/AuthContext';
import { useRouter } from 'next/navigation';
import { getAllTasks, addTask, deleteTask, updateTask, Task } from '../lib/api';
import TaskForm from '../components/TaskForm';
import TaskList from '../components/TaskList';

export default function Home() {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);
  const { token, user, logout, loading: authLoading } = useAuth();
  const router = useRouter();

  useEffect(() => {
    if (!authLoading && !token) {
      router.push('/login');
    }
  }, [token, authLoading, router]);

  const fetchTasks = useCallback(async () => {
    if (!token) return;
    setLoading(true);
    setError(null);
    try {
      const data: Task[] = await getAllTasks();
      setTasks(data);
    } catch (e: any) {
      setError(e.message);
    } finally {
      setLoading(false);
    }
  }, [token]);

  useEffect(() => {
    if (token) {
      fetchTasks();
    }
  }, [token, fetchTasks]);

  const handleAddTask = async (name: string, description: string) => {
    try {
      await addTask(name, description);
      await fetchTasks();
    } catch (e: any) {
      throw e;
    }
  };

  const handleDeleteTask = async (id: string) => {
    try {
      await deleteTask(id);
      await fetchTasks();
    } catch (e: any) {
      throw e;
    }
  };

  const handleUpdateTask = async (id: string, name: string, description: string, completed: boolean) => {
    try {
      await updateTask(id, name, description, completed);
      await fetchTasks();
    } catch (e: any) {
      throw e;
    }
  };
  
  // The toggle functionality can be part of update
  const handleToggleTask = async (id: string, completed: boolean) => {
    const task = tasks.find(t => t.id === id);
    if(task){
      await handleUpdateTask(id, task.name, task.description, completed);
    }
  };


  if (authLoading || loading) {
    return <div className="p-4">Loading...</div>;
  }

  if (!token || !user) {
    return null; // or a loading spinner, since the redirect is happening
  }
  
  if (error) {
    return <div className="p-4 text-red-500">Error: {error}</div>;
  }

  return (
    <div className="min-h-screen bg-gray-100 flex flex-col items-center justify-center p-4">
      <div className="w-full max-w-2xl">
        <div className="flex justify-between items-center mb-4">
          <h1 className="text-2xl font-bold">Welcome, {user.username}</h1>
          <button onClick={logout} className="p-2 bg-red-500 text-white rounded">Logout</button>
        </div>
        <TaskForm onAddTask={handleAddTask} />
        <TaskList 
          tasks={tasks} 
          onToggleTask={handleToggleTask} 
          onDeleteTask={handleDeleteTask} 
          onUpdateTask={handleUpdateTask} 
        />
      </div>
    </div>
  );
}