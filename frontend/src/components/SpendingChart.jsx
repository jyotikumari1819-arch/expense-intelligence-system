import { PieChart, Pie, Cell, Tooltip, Legend, ResponsiveContainer } from "recharts";

const COLORS = ["#2F5233", "#C9A227", "#B34434", "#5C5A52", "#7A9471", "#8C6D1F", "#8A5A4E", "#A8A296", "#4A6B4E", "#3D3B35"];

export default function SpendingChart({ byCategory }) {
  const data = Object.entries(byCategory || {}).map(([name, value]) => ({ name, value }));

  if (data.length === 0) {
    return <p className="empty">No data to chart yet.</p>;
  }

  return (
    <ResponsiveContainer width="100%" height={280}>
      <PieChart>
        <Pie data={data} dataKey="value" nameKey="name" outerRadius={100} label>
          {data.map((_, i) => (
            <Cell key={i} fill={COLORS[i % COLORS.length]} />
          ))}
        </Pie>
        <Tooltip formatter={(value) => `₹${value.toFixed(2)}`} />
        <Legend />
      </PieChart>
    </ResponsiveContainer>
  );
}
