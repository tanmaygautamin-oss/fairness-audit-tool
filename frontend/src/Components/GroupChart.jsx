// GroupChart.jsx
// WHAT: Renders a bar chart comparing a chosen metric (e.g. selection rate)
// across the different demographic groups, using Recharts.

import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, CartesianGrid } from "recharts";

export default function GroupChart({ perGroupData, metricKey, title }) {
    const chartData = Object.entries(perGroupData[metricKey] || {}).map(([group, value]) => ({
        group,
        value: Number(value.toFixed(3))
    }));
    
    return (
        <div className="chart-container">

            <h4>{title}</h4>
            <ResponsiveContainer width="100%" height={250}>
                <BarChart data={chartData}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="group" />
                    <YAxis />
                    <Tooltip />
                    <Bar dataKey="value" fill="#0b3d91" radius={[6, 6, 0, 0]} />
                </BarChart>
            </ResponsiveContainer>
        </div>
    );
}
