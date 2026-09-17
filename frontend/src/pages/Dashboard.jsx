import { useEffect, useState, useCallback } from "react";
import { useNavigate } from "react-router-dom";
import { api } from "../api.js";
import ExpenseForm from "../components/ExpenseForm.jsx";
import ExpenseList from "../components/ExpenseList.jsx";
import SpendingChart from "../components/SpendingChart.jsx";
import InsightsPanel from "../components/InsightsPanel.jsx";

export default function Dashboard() {
  const [expenses, setExpenses] = useState([]);
  const [insightData, setInsightData] = useState(null);
  const navigate = useNavigate();

  const now = new Date();

  const refresh = useCallback(async () => {
    const list = await api.getExpenses({ month: now.getMonth() + 1, year: now.getFullYear() });
    setExpenses(list);
    const insight = await api.getMonthlyInsight(now.getMonth() + 1, now.getFullYear());
    setInsightData(insight);
  }, []);

  useEffect(() => {
    refresh();
  }, [refresh]);

  const handleLogout = () => {
    localStorage.removeItem("token");
    navigate("/login");
  };

  return (
    <div className="dashboard">
      <header>
        <h1>Expense Intelligence System</h1>
        <button onClick={handleLogout}>Log Out</button>
      </header>

      <ExpenseForm onAdded={refresh} />

      <div className="dashboard-grid">
        <div>
          <ExpenseList expenses={expenses} onDeleted={refresh} />
        </div>
        <div>
          <SpendingChart byCategory={insightData?.by_category} />
          <InsightsPanel
            insight={insightData?.insight}
            total={insightData?.total}
            count={insightData?.transaction_count}
          />
        </div>
      </div>
    </div>
  );
}
