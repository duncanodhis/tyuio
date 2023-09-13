import React, { useEffect, useState } from 'react'
import axios from 'axios'
import { CCard, CCardBody, CCardHeader } from '@coreui/react'
import { CChartPolarArea } from '@coreui/react-chartjs'

function PolarAreaChart() {
  const [chartData, setChartData] = useState({
    labels: [],
    datasets: [
      {
        data: [],
        backgroundColor: [],
      },
    ],
  })

  useEffect(() => {
    // Fetch data from the API endpoint
    axios
      .get('http://127.0.0.1:5000/api/sales-by-category')
      .then((response) => {
        const data = response.data.sales_by_category // Access the sales data array
        const labels = data.map((item) => item.category_name)
        const salesData = data.map((item) => item.total_sales)
        const backgroundColors = generateRandomColors(data.length)

        setChartData({
          labels: labels,
          datasets: [
            {
              data: salesData,
              backgroundColor: backgroundColors,
            },
          ],
        })
      })
      .catch((error) => {
        console.error('Error fetching data:', error)
      })
  }, [])

  function generateRandomColors(count) {
    const colors = []
    for (let i = 0; i < count; i++) {
      const randomColor = `#${Math.floor(Math.random() * 16777215).toString(16)}`
      colors.push(randomColor)
    }
    return colors
  }

  return (
    <CCard className="mb-4">
      <CCardHeader>Sales by Category</CCardHeader>
      <CCardBody>
        <CChartPolarArea data={chartData} />
      </CCardBody>
    </CCard>
  )
}

export default PolarAreaChart
