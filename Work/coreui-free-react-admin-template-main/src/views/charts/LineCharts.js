import React, { useEffect, useState } from 'react'
import axios from 'axios'
import { CCard, CCardBody, CCardHeader } from '@coreui/react'
import { CChartLine } from '@coreui/react-chartjs'

function LineCharts() {
  const [salesData, setSalesData] = useState([])
  const [retentionData, setRetentionData] = useState([])
  const [returnRateData, setReturnRateData] = useState([])
  const [averageOrderValueData, setAverageOrderValueData] = useState([])

  useEffect(() => {
    // Fetch Sales Data
    axios
      .get('http://127.0.0.1:5000/api/sales')
      .then((response) => {
        setSalesData(response.data)
      })
      .catch((error) => {
        console.error('Error fetching sales data:', error)
      })

    // Fetch Retention Data
    axios
      .get('http://127.0.0.1:5000/api/retention')
      .then((response) => {
        setRetentionData(response.data)
      })
      .catch((error) => {
        console.error('Error fetching retention data:', error)
      })

    // Fetch Return Rate Data
    axios
      .get('http://127.0.0.1:5000/api/rating')
      .then((response) => {
        setReturnRateData(response.data)
      })
      .catch((error) => {
        console.error('Error fetching return rate data:', error)
      })

    // Fetch Average Order Value Data
    axios
      .get('http://127.0.0.1:5000/api/averageordervalue')
      .then((response) => {
        setAverageOrderValueData(response.data)
      })
      .catch((error) => {
        console.error('Error fetching average order value data:', error)
      })
  }, [])

  // Check if all data is available before rendering the chart
  if (
    salesData.length === 0 ||
    retentionData.length === 0 ||
    returnRateData.length === 0 ||
    averageOrderValueData.length === 0
  ) {
    return null // Return nothing if any of the data is not available
  }

  return (
    <CCard className="mb-4">
      <CCardHeader>Line Chart</CCardHeader>
      <CCardBody>
        <CChartLine
          data={{
            labels: salesData.map((record) => record.period),
            datasets: [
              {
                label: 'Sales',
                backgroundColor: 'rgba(220, 220, 220, 0.2)',
                borderColor: 'rgba(220, 220, 220, 1)',
                pointBackgroundColor: 'rgba(220, 220, 220, 1)',
                pointBorderColor: '#fff',
                data: salesData.map((record) => record.sales),
              },
              {
                label: 'Retention Rate',
                backgroundColor: 'rgba(151, 187, 205, 0.2)',
                borderColor: 'rgba(151, 187, 205, 1)',
                pointBackgroundColor: 'rgba(151, 187, 205, 1)',
                pointBorderColor: '#fff',
                data: retentionData.map((record) => record.retention_rate),
              },
              {
                label: 'Return Rate',
                backgroundColor: 'rgba(0, 255, 0, 0.2)',
                borderColor: 'rgba(0, 255, 0, 1)',
                pointBackgroundColor: 'rgba(0, 255, 0, 1)',
                pointBorderColor: '#fff',
                data: returnRateData.map((record) => record.return_rate),
              },
              {
                label: 'Average Order Value',
                backgroundColor: 'rgba(0, 0, 255, 0.2)',
                borderColor: 'rgba(0, 0, 255, 1)',
                pointBackgroundColor: 'rgba(0, 0, 255, 1)',
                pointBorderColor: '#fff',
                data: averageOrderValueData.map((record) => record.average_order_value),
              },
            ],
          }}
        />
      </CCardBody>
    </CCard>
  )
}

export default LineCharts
