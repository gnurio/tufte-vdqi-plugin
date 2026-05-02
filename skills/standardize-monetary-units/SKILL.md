---
name: standardize-monetary-units
description: Adjust time-series currency data for inflation to reveal real purchasing power
---

# Standardize Monetary Units

## Quick Start
Invoke with: `/standardize-monetary-units` and provide the required inputs.

## Purpose
Adjust time-series currency data for inflation to reveal real purchasing power

## Inputs
- **nominal_values** (`array`): Raw currency values over time
- **years** (`array`): Years corresponding to values
- **currency_region** (`string`): Currency region (e.g., US, UK, EU)

## Outputs
- **real_values** (`array`): Inflation-adjusted currency values
- **base_year** (`integer`): Base year used for adjustment

## Decision Logic

1. **Determine base year**: Use the most recent year in the dataset
2. **Fetch inflation index**: Use CPI data for the specified currency region
3. **Calculate deflator**: For each year, compute index_ratio = base_year_index / year_index
4. **Apply adjustment**: real_value = nominal_value * index_ratio
5. **Flag hyperinflation**: If annual inflation > 100%, recommend monthly/daily indices

**Formula:**
```
real_value(t) = nominal_value(t) × (CPI(base_year) / CPI(t))
```

**Regions supported:**
- US: Consumer Price Index (CPI-U)
- UK: Consumer Prices Index (CPI)
- EU: Harmonised Index of Consumer Prices (HICP)
- Other: Approximate using available index data

**Important:** Always label output as "inflation-adjusted" or "real (base_year) dollars"

## Success Criteria
Adjusted curve accurately reflects real value, not currency devaluation

## Failure Modes
- Using wrong base year
- Applying uniform adjustment to localized data
- Failing to label as inflation-adjusted

## Edge Cases
- Short-term charts where inflation is negligible
- Hyperinflation requiring daily indices

## Examples

### Example 1: US Salary Adjustment
Input: nominal=[10000, 15000], years=[2010, 2020], region="US"
Output: real_values=[12360, 15000], base_year=2020
The 2010 salary is worth $12,360 in 2020 dollars.

### Example 2: Short-term (minimal adjustment)
Input: nominal=[50000, 52000], years=[2022, 2023], region="US"
Output: real_values=[50000, 52525], base_year=2022
Small inflation adjustment over single year.

## Implementation

```python
def standardize_monetary_units(nominal_values, years, currency_region):
    """
    Adjust time-series currency data for inflation.
    
    Returns inflation-adjusted values and base year used.
    """
    # Simplified CPI data (approximate values for demonstration)
    # In production, this would fetch from official sources
    cpi_data = {
        "US": {
            2000: 172.2, 2005: 195.3, 2010: 218.1, 2014: 236.7,
            2018: 251.1, 2020: 260.3, 2021: 270.9, 2022: 292.7, 2023: 304.7
        },
        "UK": {
            2000: 71.5, 2005: 76.2, 2010: 87.6, 2015: 100.0,
            2020: 108.8, 2021: 111.6, 2022: 121.8, 2023: 127.1
        },
        "EU": {
            2000: 75.9, 2005: 81.6, 2010: 91.0, 2015: 100.0,
            2020: 105.6, 2021: 108.3, 2022: 116.5, 2023: 121.5
        }
    }
    
    # Use US as default if region not found
    cpi = cpi_data.get(currency_region, cpi_data["US"])
    
    # Determine base year (most recent)
    base_year = max(years)
    base_cpi = cpi.get(base_year, 100.0)
    
    real_values = []
    hyperinflation_warning = None
    
    for nominal, year in zip(nominal_values, years):
        year_cpi = cpi.get(year, base_cpi)
        
        # Calculate real value
        if year_cpi > 0:
            real_value = nominal * (base_cpi / year_cpi)
            real_values.append(round(real_value, 0))
        else:
            real_values.append(nominal)
        
        # Check for hyperinflation (>100% annual)
        if year < base_year:
            next_year_cpi = cpi.get(year + 1, year_cpi)
            if year_cpi > 0 and (next_year_cpi - year_cpi) / year_cpi > 1.0:
                hyperinflation_warning = "Hyperinflation detected - monthly/daily indices recommended"
    
    result = {
        "real_values": real_values,
        "base_year": base_year
    }
    
    if hyperinflation_warning:
        result["warning"] = hyperinflation_warning
    
    return result
```

## Related Skills
- calculate-lie-factor
- assess-graphical-excellence
- erase-non-data-ink
