from .schemas import Assumptions, Outputs, AuditLine

def run_appraisal(a: Assumptions) -> Outputs:
    # Revenue
    gdv = a.revenue.sellable_area_m2 * a.revenue.exit_price_per_m2

    # Base build cost
    build = a.revenue.sellable_area_m2 * a.costs.build_cost_per_m2
    contingency = build * a.costs.contingency_rate
    prof_fees = build * a.costs.professional_fees_rate
    marketing = gdv * a.costs.marketing_rate_on_gdv

    tdc_ex_land = build + contingency + prof_fees + marketing

    # Target profit
    if a.profit_target.basis == "gdv":
        target_profit = gdv * a.profit_target.target_rate
    else:
        target_profit = tdc_ex_land * a.profit_target.target_rate

    # Residual Land Value (simple residual; finance/cashflow comes next phase)
    rlv = gdv - tdc_ex_land - target_profit

    profit = target_profit
    profit_margin = (profit / gdv) if gdv > 0 else 0.0

    audit = [
        AuditLine(section="Revenue", key="gdv", label="Gross Development Value (GDV)", value=gdv,
                  formula="sellable_area_m2 * exit_price_per_m2"),
        AuditLine(section="Costs", key="build", label="Build cost", value=build,
                  formula="sellable_area_m2 * build_cost_per_m2"),
        AuditLine(section="Costs", key="contingency", label="Contingency", value=contingency,
                  formula="build * contingency_rate"),
        AuditLine(section="Costs", key="prof_fees", label="Professional fees", value=prof_fees,
                  formula="build * professional_fees_rate"),
        AuditLine(section="Costs", key="marketing", label="Marketing", value=marketing,
                  formula="gdv * marketing_rate_on_gdv"),
        AuditLine(section="Profit", key="target_profit", label="Target profit", value=target_profit,
                  formula="gdv*rate OR tdc*rate"),
        AuditLine(section="Land", key="rlv", label="Residual land value", value=rlv,
                  formula="gdv - (costs ex land) - target_profit"),
    ]

    return Outputs(
        gdv=gdv,
        tdc=tdc_ex_land,
        profit=profit,
        profit_margin=profit_margin,
        residual_land_value=rlv,
        audit=audit,
    )
