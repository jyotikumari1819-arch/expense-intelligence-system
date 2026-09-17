import { useState, useEffect } from "react";
import { api } from "../api.js";

export default function ExpenseForm({ onAdded }) {
  const [amount, setAmount] = useState("");
  const [description, setDescription] = useState("");
  const [category, setCategory] = useState("");
  const [categories, setCategories] = useState([]);
  const [submitting, setSubmitting] = useState(false);

  useEffect(() => {
    api.getCategories().then((res) => setCategories(res.categories)).catch(() => {});
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setSubmitting(true);
    try {
      await api.createExpense({
        amount: parseFloat(amount),
        description,
        category: category || undefined, // let AI categorize if left blank
      });
      setAmount("");
      setDescription("");
      setCategory("");
      onAdded();
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="expense-form">
      <input
        type="number"
        step="0.01"
        placeholder="Amount"
        value={amount}
        onChange={(e) => setAmount(e.target.value)}
        required
      />
      <input
        type="text"
        placeholder="Description (e.g. Swiggy dinner order)"
        value={description}
        onChange={(e) => setDescription(e.target.value)}
        required
      />
      <select value={category} onChange={(e) => setCategory(e.target.value)}>
        <option value="">Auto-categorize with AI</option>
        {categories.map((c) => (
          <option key={c} value={c}>{c}</option>
        ))}
      </select>
      <button type="submit" disabled={submitting}>
        {submitting ? "Adding..." : "Add Expense"}
      </button>
    </form>
  );
}
