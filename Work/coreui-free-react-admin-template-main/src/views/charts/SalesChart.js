import React, { useEffect, useState } from 'react'
import axios from 'axios'
import { CCard, CCardBody, CCol, CCardHeader } from '@coreui/react'
import { CChartBar } from '@coreui/react-chartjs'

function SalesChart() {
  const [salesData, setSalesData] = useState([])

  useEffect(() => {
    axios
      .get('http://127.0.0.1:5000/api/sales')
      .then((response) => {
        setSalesData(response.data)
      })
      .catch((error) => {
        console.error('Error fetching sales data:', error)
      })
  }, [])

  // Create arrays for labels and sales data
  const chartLabels = salesData.map((record) => record.period)
  const chartSalesData = salesData.map((record) => record.sales)

  // Render the bar chart using dynamic labels
  return (
    <CCol xs={6}>
      <CCard className="mb-4">
        <CCardHeader>Bar Chart</CCardHeader>
        <CCardBody>
          <CChartBar
            data={{
              labels: chartLabels,
              datasets: [
                {
                  label: 'Sales over time',
                  backgroundColor: '#f87979',
                  data: chartSalesData,
                },
              ],
            }}
          />
        </CCardBody>
      </CCard>
    </CCol>
  )
}

export default SalesChart
