import React, { useState, useEffect } from 'react'
import { CRow, CCol, CDropdown, CDropdownToggle, CWidgetStatsA } from '@coreui/react'
import { getStyle } from '@coreui/utils'
import { CChartLine } from '@coreui/react-chartjs'
import CIcon from '@coreui/icons-react'
import { cilArrowBottom, cilArrowTop } from '@coreui/icons'

const WidgetsDropdown = () => {
  const [customerData, setCustomerData] = useState([])
  const [incomeData, setIncomeData] = useState([])
  const [currencyValue, setCurrencyValue] = useState(null)
  const [historicalCurrencyData, setHistoricalCurrencyData] = useState([])

  useEffect(() => {
    fetch('http://127.0.0.1:5000/api/customersDetails')
      .then((response) => response.json())
      .then((data) => setCustomerData(data))
      .catch((error) => console.error('Error fetching customer data:', error))
  }, [])

  const calculateGrowth = () => {
    if (customerData.length < 2) return 0
    const initialValue = customerData[0].count
    const finalValue = customerData[customerData.length - 1].count
    return ((finalValue - initialValue) / initialValue) * 100
  }

  useEffect(() => {
    fetch('/api/income')
      .then((response) => response.json())
      .then((data) => setIncomeData(data))
      .catch((error) => console.error('Error fetching income data:', error))
  }, [])

  const calculateIncomeGrowth = () => {
    if (incomeData.length < 2) return 0
    const initialValue = incomeData[0].value
    const finalValue = incomeData[incomeData.length - 1].value
    return ((finalValue - initialValue) / initialValue) * 100
  }

  const fetchLatestCurrencyValue = () => {
    fetch(
      'https://api.currencyapi.com/v3/latest?apikey=cur_live_DNn7nlFz3HLQEAiRofwk6M9kCT6MhUjIE8UvJgwu&currencies=GEL&base_currency=BTC',
    )
      .then((response) => response.json())
      .then((data) => {
        const gelValue = data.data.GEL.value
        setCurrencyValue(gelValue)
        fetchHistoricalCurrencyData(gelValue)
      })
      .catch((error) => console.error('Error fetching latest currency data:', error))
  }

  useEffect(() => {
    fetchLatestCurrencyValue()
  })

  const fetchHistoricalCurrencyData = (latestValue) => {
    const today = new Date()
    const historicalDates = [
      getPreviousDate(today, 1), // Yesterday
      getPreviousDate(today, 2), // The day before yesterday
      // Add more historical dates as needed
    ]

    const historicalDataPromises = historicalDates.map((date) => fetchHistoricalDataForDate(date))

    Promise.all(historicalDataPromises)
      .then((historicalDataArray) => {
        const historicalValues = historicalDataArray.map(
          (historicalData) => historicalData.data.GEL.value,
        )
        setHistoricalCurrencyData(historicalValues)
      })
      .catch((error) => console.error('Error fetching historical currency data:', error))
  }

  const getPreviousDate = (currentDate, daysAgo) => {
    const prevDate = new Date(currentDate)
    prevDate.setDate(currentDate.getDate() - daysAgo)
    return prevDate.toISOString().slice(0, 10) // Format as "YYYY-MM-DD"
  }

  const fetchHistoricalDataForDate = (date) => {
    return fetch(
      `https://api.currencyapi.com/v3/historical?apikey=cur_live_DNn7nlFz3HLQEAiRofwk6M9kCT6MhUjIE8UvJgwu&currencies=GEL&base_currency=BTC&date=${date}`,
    ).then((response) => response.json())
  }

  const calculatePercentageChange = () => {
    if (currencyValue !== null && historicalCurrencyData.length > 0) {
      const previousDayValue = historicalCurrencyData[0]
      const percentageChange = ((currencyValue - previousDayValue) / previousDayValue) * 100
      return percentageChange
    }
    return 0
  }
  return (
    <CRow>
      <CCol sm={6} lg={3}>
        <CWidgetStatsA
          className="mb-4"
          color="primary"
          value={
            <>
              {customerData.length > 0 && (
                <>
                  {customerData[customerData.length - 1].count}{' '}
                  <span className="fs-6 fw-normal">
                    ({calculateGrowth().toFixed(1)}%{' '}
                    {calculateGrowth() > 0 ? (
                      <CIcon icon="cilArrowTop" />
                    ) : (
                      <CIcon icon="cilArrowBottom" />
                    )}
                    )
                  </span>
                </>
              )}
            </>
          }
          title="Customers"
          action={
            <CDropdown alignment="end">
              <CDropdownToggle color="transparent" caret={false} className="p-0">
                <CIcon className="text-high-emphasis-inverse" />
              </CDropdownToggle>
            </CDropdown>
          }
          chart={
            <CChartLine
              className="mt-3 mx-3"
              style={{ height: '70px' }}
              data={{
                labels: customerData.map((entry) => entry.label), // Use your own labels here
                datasets: [
                  {
                    label: 'Customer Growth',
                    backgroundColor: 'transparent',
                    borderColor: 'rgba(255,255,255,.55)',
                    pointBackgroundColor: getStyle('--cui-primary'),
                    data: customerData.map((entry) => entry.count),
                  },
                ],
              }}
              options={{
                plugins: {
                  legend: {
                    display: false,
                  },
                },
                maintainAspectRatio: false,
                scales: {
                  x: {
                    grid: {
                      display: false,
                      drawBorder: false,
                    },
                    ticks: {
                      display: false,
                    },
                  },
                  y: {
                    min: 0, // Adjust this to your preferred minimum value
                    beginAtZero: true,
                    display: false,
                    grid: {
                      display: false,
                    },
                    ticks: {
                      display: false,
                    },
                  },
                },
                elements: {
                  line: {
                    borderWidth: 1,
                    tension: 0.4,
                  },
                  point: {
                    radius: 4,
                    hitRadius: 10,
                    hoverRadius: 4,
                  },
                },
              }}
            />
          }
        />
      </CCol>
      <CCol sm={6} lg={3}>
        <CWidgetStatsA
          className="mb-4"
          color="info"
          value={
            <>
              {incomeData.length > 0 && (
                <>
                  ${incomeData[incomeData.length - 1].value.toFixed(2)}{' '}
                  <span className="fs-6 fw-normal">
                    ({calculateIncomeGrowth().toFixed(1)}%{' '}
                    {calculateIncomeGrowth() > 0 ? (
                      <CIcon icon="cilArrowTop" />
                    ) : (
                      <CIcon icon="cilArrowBottom" />
                    )}
                    )
                  </span>
                </>
              )}
            </>
          }
          title="Income"
          action={
            <CDropdown alignment="end">
              <CDropdownToggle color="transparent" caret={false} className="p-0">
                <CIcon className="text-high-emphasis-inverse" />
              </CDropdownToggle>
            </CDropdown>
          }
          chart={
            <CChartLine
              className="mt-3 mx-3"
              style={{ height: '70px' }}
              data={{
                labels: incomeData.map((entry) => entry.label),
                datasets: [
                  {
                    label: 'Income',
                    backgroundColor: 'transparent',
                    borderColor: 'rgba(255,255,255,.55)',
                    pointBackgroundColor: 'your-color-here',
                    data: incomeData.map((entry) => entry.value),
                  },
                ],
              }}
              options={{
                plugins: {
                  legend: {
                    display: false,
                  },
                },
                maintainAspectRatio: false,
                scales: {
                  x: {
                    grid: {
                      display: false,
                      drawBorder: false,
                    },
                    ticks: {
                      display: false,
                    },
                  },
                  y: {
                    min: 0, // Adjust this to your preferred minimum value
                    // max: ..., // Adjust this if needed
                    display: false,
                    grid: {
                      display: false,
                    },
                    ticks: {
                      display: false,
                    },
                  },
                },
                elements: {
                  line: {
                    borderWidth: 1,
                  },
                  point: {
                    radius: 4,
                    hitRadius: 10,
                    hoverRadius: 4,
                  },
                },
              }}
            />
          }
        />
      </CCol>
      <CCol sm={6} lg={3}>
        <CWidgetStatsA
          className="mb-4"
          color="warning"
          value={
            <>
              {currencyValue !== null ? (
                <>
                  {currencyValue.toFixed(2)}{' '}
                  <span className="fs-6 fw-normal">
                    {calculatePercentageChange().toFixed(1)}%{' '}
                    {calculatePercentageChange() > 0 ? (
                      <CIcon icon={cilArrowTop} />
                    ) : (
                      <CIcon icon={cilArrowBottom} />
                    )}
                  </span>
                </>
              ) : (
                'Loading...'
              )}
            </>
          }
          title="BTC/GEL"
          action={
            <CDropdown alignment="end">
              <CDropdownToggle color="transparent" caret={false} className="p-0">
                <CIcon className="text-high-emphasis-inverse" />
              </CDropdownToggle>
            </CDropdown>
          }
          chart={
            <CChartLine
              className="mt-3"
              style={{ height: '70px' }}
              data={{
                labels: ['Yesterday', 'Day Before Yesterday'], // Labels for historical dates
                datasets: [
                  {
                    label: 'Currency Value',
                    backgroundColor: 'rgba(255,255,255,.2)',
                    borderColor: 'rgba(255,255,255,.55)',
                    data: historicalCurrencyData,
                    fill: true,
                  },
                ],
              }}
              options={{
                plugins: {
                  legend: {
                    display: false,
                  },
                },
                maintainAspectRatio: false,
                scales: {
                  x: {
                    display: false,
                  },
                  y: {
                    display: false,
                  },
                },
                elements: {
                  line: {
                    borderWidth: 2,
                    tension: 0.4,
                  },
                  point: {
                    radius: 0,
                    hitRadius: 10,
                    hoverRadius: 4,
                  },
                },
              }}
            />
          }
        />
      </CCol>
    </CRow>
  )
}
export default WidgetsDropdown
