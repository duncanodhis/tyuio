/* eslint-disable prettier/prettier */
import React, { useEffect, useState } from 'react'
import axios from 'axios'
import { CChart } from '@coreui/react-chartjs'
import { CCard, CCardBody, CCardHeader } from '@coreui/react'
function getStyle(property) {
  return getComputedStyle(document.documentElement).getPropertyValue(property).trim();
}

function DoughnutChart() {
  const [chartData, setChartData] = useState({
    labels: [],
    datasets: [
      {
        backgroundColor: [],
        data: [],
      },
    ],
  })

  useEffect(() => {
    // Fetch data from the API endpoint
    axios
      .get('http://127.0.0.1:5000/api/revenue-distribution-by-product')
      .then((response) => {
        const data = response.data
        const productNames = data.map((item) => item.product_name)
        const revenueData = data.map((item) => item.revenue)
        const backgroundColors = generateRandomColors(data.length)

        setChartData({
          labels: productNames,
          datasets: [
            {
              backgroundColor: backgroundColors,
              data: revenueData,
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
      <CCardHeader>Revenue Distribution by Product (Doughnut Chart)</CCardHeader>
      <CCardBody>
      <CChart
      type="doughnut"
      data={chartData}
      options={{
        plugins: {
          legend: {
            labels: {
              color: getStyle('--cui-body-color'),
            },
          },
        },
      }}
    />
      </CCardBody>
    </CCard>

  )
}

export default DoughnutChart
