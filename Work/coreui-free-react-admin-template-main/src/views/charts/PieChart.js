import React, { useEffect, useState } from 'react'
import axios from 'axios'
import { CCard, CCardHeader, CCardBody } from '@coreui/react'
import { CChartPie } from '@coreui/react-chartjs'

function CustomerSegmentationPieChart() {
  const [segmentationData, setSegmentationData] = useState([])

  useEffect(() => {
    // Fetch customer segmentation data based on location and spending habits
    axios
      .get('http://127.0.0.1:5000/api/customer-segmentation')
      .then((response) => {
        setSegmentationData(response.data)
      })
      .catch((error) => {
        console.error('Error fetching customer segmentation data:', error)
      })
  }, [])

  // Format the data for the pie chart
  const pieChartData = {
    labels: segmentationData.map((segment) => segment.product_name), // Labels represent product names
    datasets: [
      {
        data: segmentationData.map((segment) => segment.order_count), // Values represent the order count for each product
        backgroundColor: generateRandomColors(segmentationData.length), // Generate random colors
        hoverBackgroundColor: generateRandomColors(segmentationData.length), // Generate random hover colors
      },
    ],
  }

  // Function to generate random colors
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
      <CCardHeader>Customer Segmentation</CCardHeader>
      <CCardBody>
        <CChartPie data={pieChartData} />
      </CCardBody>
    </CCard>
  )
}

export default CustomerSegmentationPieChart
