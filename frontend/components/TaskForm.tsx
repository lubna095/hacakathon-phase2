// frontend/components/TaskForm.tsx
'use client';

import { useState } from 'react';

interface TaskFormProps {
  onAddTask: (name: string, description: string) => Promise<void>;
}

export default function TaskForm({ onAddTask }: TaskFormProps) {
  const [name, setName] = useState('');
  const [description, setDescription] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!name.trim() || !description.trim()) {
      setError('Task name and description cannot be empty.');
      return;
    }
    setLoading(true);
    setError(null);
    try {
      await onAddTask(name, description);
      setName('');
      setDescription('');
    } catch (err: any) {
      setError(err.message || 'Failed to add task.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="bg-white shadow-md rounded-lg p-6 w-full max-w-md mb-8">
      <h2 className="text-2xl font-bold mb-4">Add New Task</h2>
      {error && <p className="text-red-500 mb-4">{error}</p>}
      <div className="mb-4">
        <label htmlFor="name" className="block text-gray-700 text-sm font-bold mb-2">
          Task Name:
        </label>
        <input
          type="text"
          id="name"
          className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
          value={name}
          onChange={(e) => setName(e.target.value)}
          disabled={loading}
          required
        />
      </div>
      <div className="mb-6">
        <label htmlFor="description" className="block text-gray-700 text-sm font-bold mb-2">
          Description:
        </label>
        <textarea
          id="description"
          className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline h-24 resize-none"
          value={description}
          onChange={(e) => setDescription(e.target.value)}
          disabled={loading}
          required
        />
      </div>
      <button
        type="submit"
        className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline disabled:opacity-50"
        disabled={loading}
      >
        {loading ? 'Adding...' : 'Add Task'}
      </button>
    </form>
  );
}