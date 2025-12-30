// frontend/components/TaskItem.tsx
'use client';

import { useState } from 'react';
import { Task } from '../lib/api';

interface TaskItemProps {
  task: Task;
  onToggle: (id: string, completed: boolean) => Promise<void>;
  onDelete: (id: string) => Promise<void>;
  onUpdate: (id: string, name: string, description: string, completed: boolean) => Promise<void>;
}

export default function TaskItem({ task, onToggle, onDelete, onUpdate }: TaskItemProps) {
  const [isEditing, setIsEditing] = useState(false);
  const [editedName, setEditedName] = useState(task.name);
  const [editedDescription, setEditedDescription] = useState(task.description);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleToggle = async () => {
    setLoading(true);
    setError(null);
    try {
      await onToggle(task.id, !task.completed);
    } catch (err: any) {
      setError(err.message || 'Failed to toggle task.');
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async () => {
    setLoading(true);
    setError(null);
    try {
      await onDelete(task.id);
    } catch (err: any) {
      setError(err.message || 'Failed to delete task.');
    } finally {
      setLoading(false);
    }
  };

  const handleUpdate = async () => {
    setLoading(true);
    setError(null);
    try {
      await onUpdate(task.id, editedName, editedDescription, task.completed);
      setIsEditing(false);
    } catch (err: any) {
      setError(err.message || 'Failed to update task.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <li className="flex flex-col bg-gray-50 shadow rounded-lg p-4 mb-2 last:mb-0">
      {error && <p className="text-red-500 mb-2">{error}</p>}
      {isEditing ? (
        <div className="flex flex-col w-full">
          <input
            type="text"
            className="shadow appearance-none border rounded w-full py-1 px-2 text-gray-700 mb-2"
            value={editedName}
            onChange={(e) => setEditedName(e.target.value)}
            disabled={loading}
          />
          <textarea
            className="shadow appearance-none border rounded w-full py-1 px-2 text-gray-700 mb-2 resize-none"
            value={editedDescription}
            onChange={(e) => setEditedDescription(e.target.value)}
            disabled={loading}
          />
          <div className="flex justify-end gap-2">
            <button
              onClick={handleUpdate}
              className="bg-green-500 hover:bg-green-700 text-white font-bold py-1 px-2 rounded text-sm disabled:opacity-50"
              disabled={loading}
            >
              Save
            </button>
            <button
              onClick={() => setIsEditing(false)}
              className="bg-gray-500 hover:bg-gray-700 text-white font-bold py-1 px-2 rounded text-sm disabled:opacity-50"
              disabled={loading}
            >
              Cancel
            </button>
          </div>
        </div>
      ) : (
        <div className="flex justify-between items-center w-full">
          <div className="flex items-center flex-grow">
            <input
              type="checkbox"
              checked={task.completed}
              onChange={handleToggle}
              className="mr-2 h-5 w-5"
              disabled={loading}
            />
            <div>
              <h3 className={`text-lg font-semibold ${task.completed ? 'line-through text-gray-500' : 'text-gray-900'}`}>
                {task.name}
              </h3>
              <p className={`text-sm ${task.completed ? 'line-through text-gray-400' : 'text-gray-600'}`}>
                {task.description}
              </p>
            </div>
          </div>
          <div className="flex gap-2">
            <button
              onClick={() => setIsEditing(true)}
              className="bg-yellow-500 hover:bg-yellow-700 text-white font-bold py-1 px-2 rounded text-sm disabled:opacity-50"
              disabled={loading}
            >
              Edit
            </button>
            <button
              onClick={handleDelete}
              className="bg-red-500 hover:bg-red-700 text-white font-bold py-1 px-2 rounded text-sm disabled:opacity-50"
              disabled={loading}
            >
              Delete
            </button>
          </div>
        </div>
      )}
    </li>
  );
}