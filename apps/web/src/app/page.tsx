"use client";

import { useEffect, useMemo, useState } from "react";
import { useForm } from "react-hook-form";
import { postJSON } from "@/lib/api";

type Assumptions = {
  revenue: { sellable_area_m2: number; exit_price_per_m2: number };
  costs: {
    build_cost_per_m2: number;
    contingency_rate: number;
    professional_fees_rate: number;
    marketing_rate_on_gdv: number;
  };
  profit_target: { basis: "gdv" | "cost"; target_rate: number };
};

type Output = {
  gdv: number;
  tdc: number;
  profit: number;
  profit_margin: number;
  residual_land_value: number;
  audit: { section: string; key: string; label: string; value: number; formula: string }[];
};

function money(x: number) {
  return new Intl.NumberFormat(undefined, { style: "currency", currency: "GBP", maximumFractionDigits: 0 }).format(x);
}
function pct(x: number) {
  return new Intl.NumberFormat(undefined, { style: "percent", maximumFractionDigits: 1 }).format(x);
}

export default function HomePage() {
  const { register, watch } = useForm<Assumptions>({
    defaultValues: {
      revenue: { sellable_area_m2: 3000, exit_price_per_m2: 4500 },
      costs: { build_cost_per_m2: 1800, contingency_rate: 0.1, professional_fees_rate: 0.1, marketing_rate_on_gdv: 0.03 },
      profit_target: { basis: "gdv", target_rate: 0.2 },
    },
    mode: "onChange",
  });

  const [out, setOut] = useState<Output | null>(null);
  const [err, setErr] = useState<string | null>(null);

  const a = watch();
  const payload = useMemo(() => a, [a]);

  useEffect(() => {
    const t = setTimeout(async () => {
      setErr(null);
      try {
        const result = await postJSON<Output>("/calculate", payload);
        setOut(result);
      } catch (e: any) {
        setErr(e?.message ?? "Error");
      }
    }, 250); // debounce
    return () => clearTimeout(t);
  }, [payload]);

  return (
    <main style={{ display: "grid", gridTemplateColumns: "420px 1fr", gap: 24, padding: 24 }}>
      <section style={{ border: "1px solid #eee", borderRadius: 12, padding: 16 }}>
        <h2>Inputs</h2>

        <h3>Revenue</h3>
        <label>Sellable area (m²)</label>
        <input type="number" step="1" {...register("revenue.sellable_area_m2", { valueAsNumber: true })} />
        <label>Exit price (£/m²)</label>
        <input type="number" step="1" {...register("revenue.exit_price_per_m2", { valueAsNumber: true })} />

        <h3>Costs</h3>
        <label>Build cost (£/m²)</label>
        <input type="number" step="1" {...register("costs.build_cost_per_m2", { valueAsNumber: true })} />
        <label>Contingency (0–0.5)</label>
        <input type="number" step="0.01" {...register("costs.contingency_rate", { valueAsNumber: true })} />
        <label>Professional fees (0–0.5)</label>
        <input type="number" step="0.01" {...register("costs.professional_fees_rate", { valueAsNumber: true })} />
        <label>Marketing on GDV (0–0.2)</label>
        <input type="number" step="0.005" {...register("costs.marketing_rate_on_gdv", { valueAsNumber: true })} />

        <h3>Profit Target</h3>
        <label>Basis</label>
        <select {...register("profit_target.basis")}>
          <option value="gdv">GDV</option>
          <option value="cost">Cost</option>
        </select>
        <label>Target rate (0–0.5)</label>
        <input type="number" step="0.01" {...register("profit_target.target_rate", { valueAsNumber: true })} />
      </section>

      <section style={{ border: "1px solid #eee", borderRadius: 12, padding: 16 }}>
        <h2>Outputs</h2>
        {err && <p style={{ color: "crimson" }}>{err}</p>}
        {!out ? (
          <p>Calculating…</p>
        ) : (
          <>
            <div style={{ display: "grid", gridTemplateColumns: "repeat(3, 1fr)", gap: 12 }}>
              <KPI title="Residual Land Value" value={money(out.residual_land_value)} />
              <KPI title="Profit" value={money(out.profit)} />
              <KPI title="Profit Margin" value={pct(out.profit_margin)} />
              <KPI title="GDV" value={money(out.gdv)} />
              <KPI title="TDC (ex land)" value={money(out.tdc)} />
              <KPI title="Implied Land Offer" value={money(out.residual_land_value)} />
            </div>

            <h3 style={{ marginTop: 18 }}>Audit trail</h3>
            <table style={{ width: "100%", borderCollapse: "collapse" }}>
              <thead>
                <tr>
                  <th align="left">Section</th>
                  <th align="left">Item</th>
                  <th align="right">Value</th>
                  <th align="left">Formula</th>
                </tr>
              </thead>
              <tbody>
                {out.audit.map((r) => (
                  <tr key={r.key} style={{ borderTop: "1px solid #eee" }}>
                    <td>{r.section}</td>
                    <td>{r.label}</td>
                    <td align="right">{money(r.value)}</td>
                    <td style={{ opacity: 0.7 }}>{r.formula}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </>
        )}
      </section>
    </main>
  );
}

function KPI({ title, value }: { title: string; value: string }) {
  return (
    <div style={{ border: "1px solid #eee", borderRadius: 12, padding: 12 }}>
      <div style={{ fontSize: 12, opacity: 0.7 }}>{title}</div>
      <div style={{ fontSize: 20, fontWeight: 700 }}>{value}</div>
    </div>
  );
}
