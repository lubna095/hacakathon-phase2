// frontend/components/TaskList.tsx
'use client';

import TaskItem from './TaskItem';
import { Task } from '../lib/api';

interface TaskListProps {
  tasks: Task[];
  onToggleTask: (id: string, completed: boolean) => Promise<void>;
  onDeleteTask: (id: string) => Promise<void>;
  onUpdateTask: (id: string, name: string, description: string, completed: boolean) => Promise<void>;
}

export default function TaskList({ tasks, onToggleTask, onDeleteTask, onUpdateTask }: TaskListProps) {
  return (
    <div className="bg-white shadow-md rounded-lg p-6 w-full max-w-md">
      <h2 className="text-2xl font-bold mb-4">Your Tasks</h2>
      {tasks.length === 0 ? (
        <p>No tasks available.</p>
      ) : (
        <ul>
          {tasks.map((task) => (
            <TaskItem
              key={task.id}
              task={task}
              onToggle={onToggleTask}
              onDelete={onDeleteTask}
              onUpdate={onUpdateTask}
            />
          ))}
        </ul>
      )}
    </div>
  );
}