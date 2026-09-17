import { api } from "../api.js";

export default function ExpenseList({ expenses, onDeleted }) {
  const handleDelete = async (id) => {
    await api.deleteExpense(id);
    onDeleted();
  };

  if (expenses.length === 0) {
    return <p className="empty">No expenses yet — add your first one above.</p>;
  }

  return (
    <table className="expense-table">
      <thead>
        <tr>
          <th>Date</th>
          <th>Description</th>
          <th>Category</th>
          <th>Amount</th>
          <th></th>
        </tr>
      </thead>
      <tbody>
        {expenses.map((e) => (
          <tr key={e.id}>
            <td>{new Date(e.date).toLocaleDateString()}</td>
            <td>{e.description}</td>
            <td><span className="category-badge">{e.category}</span></td>
            <td>₹{e.amount.toFixed(2)}</td>
            <td>
              <button className="delete-btn" onClick={() => handleDelete(e.id)}>✕</button>
            </td>
          </tr>
        ))}
      </tbody>
    </table>
  );
}
