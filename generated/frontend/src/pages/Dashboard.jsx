export default function Dashboard() {
  return (
    <div className="bg-white p-8 rounded-lg shadow-sm border border-gray-100">
      <h1 className="text-3xl font-bold text-gray-800 mb-6">Dashboard</h1>
      <p className="text-gray-600">
        This is a generated placeholder page for the <strong>Dashboard</strong> intent. 
      </p>
      <div className="mt-8 p-4 bg-indigo-50 border border-indigo-100 rounded-md">
        <p className="text-indigo-800 font-medium">To do:</p>
        <ul className="list-disc list-inside text-indigo-700 mt-2 space-y-1 text-sm">
          <li>Implement UI layout</li>
          <li>Connect to AAYU-generated backend APIs</li>
          <li>Bind entities and state</li>
        </ul>
      </div>
    </div>
  )
}
