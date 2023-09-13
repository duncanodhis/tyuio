/* eslint-disable react-hooks/exhaustive-deps */
import React, { useState, useEffect } from 'react'
import axios from 'axios'
import {
  CAvatar,
  CButton,
  CButtonGroup,
  CCard,
  CCardBody,
  CCardFooter,
  CCardHeader,
  CCol,
  CProgress,
  CRow,
  CTable,
  CTableBody,
  CTableDataCell,
  CTableHead,
  CTableHeaderCell,
  CTableRow,
} from '@coreui/react'

import { CChartLine } from '@coreui/react-chartjs'
import CIcon from '@coreui/icons-react'
import WidgetsDropdown from '../widgets/WidgetsDropdown'
import Purchase from './Purchase'
const Dashboard = () => {
  const [salesData, setSalesData] = useState({ labels: [], datasets: [] })
  const [selectedPeriod, setSelectedPeriod] = useState('Month')
  const [tableItems, setTableItems] = useState([])
  const [tableItems1, setTableItems1] = useState([])
  const [topBuyersData, setTopBuyersData] = useState([])

  const fetchTopBuyersData = async () => {
    try {
      const response = await axios.get('http://127.0.0.1:5000/api/top-buyers') // Update with actual endpoint
      const fetchedTopBuyersData = response.data
      console.log('top buyers ', fetchedTopBuyersData)
      setTopBuyersData(fetchedTopBuyersData)
    } catch (error) {
      console.error('Error fetching top buyers data:', error)
    }
  }

  useEffect(() => {
    fetchTopBuyersData()
  }, [])

  const fetchSummaryData = async () => {
    try {
      const response = await axios.get('http://127.0.0.1:5000/api/summary') // Update with actual endpoint
      const summaryData = response.data
      const tableItems1 = [
        {
          totalValue: summaryData.total_value,
          remainingQuantity: summaryData.remaining_quantity,
          soldToday: summaryData.sold_today,
        },
      ]
      setTableItems1(tableItems1)
    } catch (error) {
      console.error('Error fetching summary data:', error)
    }
  }
  useEffect(() => {
    fetchSummaryData()
  }, [])
  useEffect(() => {
    fetchSummaryData()
  }, [])

  const [metrics, setMetrics] = useState({
    sales: 0,
    earnings: 0,
    profitMargin: 0,
    avgOrderValue: 0,
    customerLifetime: 0,
  })
  const fetchSalesMetricsData = async () => {
    try {
      const earningsResponse = await axios.get('http://127.0.0.1:5000/api/earnings')
      const salesResponse = await axios.get('http://127.0.0.1:5000/api/sales')
      const clientsResponse = await axios.get('http://127.0.0.1:5000/api/clients')
      const goodsResponse = await axios.get('http://127.0.0.1:5000/api/goods')
      const earningsData = earningsResponse.data
      const salesData = salesResponse.data
      const clientsData = clientsResponse.data
      const goodsData = goodsResponse.data

      // Ensure that all data arrays have the same length
      const minLength = Math.min(
        earningsData.length,
        salesData.length,
        clientsData.length,
        goodsData.length,
      )

      // Process data and create table items based on periods
      const processedTableItems = []

      for (let index = 0; index < minLength; index++) {
        processedTableItems.push({
          period: earningsData[index].period,
          earnings: earningsData[index].earnings,
          sales: salesData[index].sales,
          clients: clientsData[index].clients,
          goods: goodsData[index].goods,
        })
      }

      setTableItems(processedTableItems)
    } catch (error) {
      console.error('Error fetching metrics data:', error)
    }
  }

  useEffect(() => {
    fetchSalesMetricsData()
  }, [])

  useEffect(() => {
    fetchSalesMetricsData()
  }, [])
  const handlePeriodChange = (period) => {
    setSelectedPeriod(period)
  }

  const fetchData = async () => {
    try {
      const response = await axios.get('http://127.0.0.1:5000/api/sales_stat', {
        params: { period: selectedPeriod }, // Pass selectedPeriod as a query parameter
      })
      const orders = response.data

      // console.log('Fetched data:', orders) // Log the fetched data

      // Process data for the chart...
      const labels = orders[selectedPeriod].map((item) => item.period) // Extract labels
      const salesValues = orders[selectedPeriod].map((item) => item.sales) // Extract sales values

      const processedData = {
        labels: labels,
        datasets: [
          {
            label: 'Sales',
            data: salesValues,
            backgroundColor: 'rgba(0,123,255,0.1)',
            borderColor: 'rgba(0,123,255,1)',
            pointHoverBackgroundColor: 'rgba(0,123,255,1)',
            borderWidth: 2,
            lineTension: 0.4,
            pointRadius: 4,
            pointHoverRadius: 4,
            pointBorderColor: 'transparent',
            pointHoverBorderColor: 'rgba(0,123,255,1)',
          },
        ],
      }
      setSalesData(processedData)

      console.log('Processed data:', processedData) // Log the processed data
    } catch (error) {
      console.error('Error fetching data:', error)
    }
  }

  useEffect(() => {
    fetchData()
  }, [selectedPeriod])

  const fetchMetricsData = async () => {
    try {
      const response = await axios.get('http://127.0.0.1:5000/api/metrics') // Adjust endpoint
      const metricsData = response.data
      setMetrics(metricsData)
    } catch (error) {
      console.error('Error fetching data:', error)
    }
  }
  useEffect(() => {
    fetchMetricsData()
  }, [])

  const metricsDisplayItems = [
    { title: 'Total Sales($)', value: metrics.sales, color: 'info' },
    { title: 'Total Earnings($)', value: metrics.earnings, color: 'success' },
    {
      title: 'Profit Margin (%)',
      value: `${(metrics.profitMargin * 100).toFixed(2)}%`,
      color: 'warning',
    },
    { title: 'Average Order Value ($)', value: metrics.avgOrderValue, color: 'primary' },
    { title: 'Customer Lifetime Value ($)', value: metrics.customerLifetime, color: 'danger' },
  ]
  return (
    <>
      <WidgetsDropdown />
      <CCard className="mb-4">
        <CCardBody>
          <CRow>
            <CCol sm={5}>
              <h4 id="traffic" className="card-title mb-0">
                Sales
              </h4>
              <div className="small text-medium-emphasis">
                {selectedPeriod === 'Day' && 'Today'}
                {selectedPeriod === 'Week' && 'This Week'}
                {selectedPeriod === 'Month' && 'This Month'}
                {selectedPeriod === '90 Days' && 'Last 90 Days'}
                {selectedPeriod === 'Half Year' && 'Last 6 Months'}
                {selectedPeriod === 'Year' && 'This Year'}
              </div>
            </CCol>
            <CCol sm={7} className="d-none d-md-block">
              <CButton color="primary" className="float-end">
                <CIcon icon="cilCloudDownload" />
              </CButton>
              <CButtonGroup className="float-end me-3">
                {['Day', 'Week', 'Month', '90 Days', 'Half Year', 'Year'].map((value) => (
                  <CButton
                    color="outline-secondary"
                    key={value}
                    className="mx-0"
                    active={value === selectedPeriod}
                    onClick={() => handlePeriodChange(value)}
                  >
                    {value}
                  </CButton>
                ))}
              </CButtonGroup>
            </CCol>
          </CRow>
          <CChartLine
            style={{ height: '300px', marginTop: '40px' }}
            data={salesData}
            options={{
              maintainAspectRatio: false,
              plugins: {
                legend: {
                  display: false,
                },
              },
              scales: {
                x: {
                  grid: {
                    drawOnChartArea: false,
                  },
                },
                y: {
                  ticks: {
                    beginAtZero: true,
                    maxTicksLimit: 5,
                    stepSize: Math.ceil(250 / 5),
                    max: 250,
                  },
                },
              },
              elements: {
                line: {
                  tension: 0.4,
                },
                point: {
                  radius: 0,
                  hitRadius: 10,
                  hoverRadius: 4,
                  hoverBorderWidth: 3,
                },
              },
            }}
          />
        </CCardBody>
        <CCardFooter>
          <CRow xs={{ cols: 1 }} md={{ cols: 5 }} className="text-center">
            {metricsDisplayItems.map((item, index) => (
              <CCol className="mb-sm-2 mb-0" key={index}>
                <div className="text-medium-emphasis">{item.title}</div>
                <strong>{item.value}</strong>
                <CProgress thin className="mt-2" color={item.color} value={item.value} />
              </CCol>
            ))}
          </CRow>
        </CCardFooter>
      </CCard>
      <CRow>
        <CCol xs>
          <CCard className="mb-4">
            <CCardHeader>Traffic {' & '} Sales</CCardHeader>
            <CCardBody>
              <br />
              <CTable align="middle" className="mb-0 border" hover responsive>
                <CTableHead color="light">
                  <CTableRow>
                    <CTableHeaderCell className="text-center">
                      <CIcon icon="cilPeople" />
                    </CTableHeaderCell>
                    <CTableHeaderCell>Period</CTableHeaderCell>
                    <CTableHeaderCell>Earnings</CTableHeaderCell>
                    <CTableHeaderCell>Sales</CTableHeaderCell>
                    <CTableHeaderCell>Clients</CTableHeaderCell>
                  </CTableRow>
                </CTableHead>
                <CTableBody>
                  {tableItems.map((item, index) => (
                    <CTableRow key={index}>
                      <CTableDataCell className="text-center">
                        <CAvatar size="md" />
                      </CTableDataCell>
                      <CTableDataCell>{item.period}</CTableDataCell>
                      <CTableDataCell>{item.earnings}</CTableDataCell>
                      <CTableDataCell>{item.sales}</CTableDataCell>
                      <CTableDataCell>{item.clients}</CTableDataCell>
                    </CTableRow>
                  ))}
                </CTableBody>
              </CTable>
              <br />
              <CTable align="middle" className="mb-0 border" hover responsive>
                <CTableHead color="light">
                  <CTableRow>
                    <CTableHeaderCell className="text-center"> Summary</CTableHeaderCell>
                    <CTableHeaderCell>Items on Sale Today</CTableHeaderCell>
                  </CTableRow>
                </CTableHead>
                <CTableBody>
                  <CTableRow>
                    <CTableDataCell className="text-center" rowSpan={4}>
                      <strong>Summary (in BTC)</strong>
                    </CTableDataCell>
                    <CTableDataCell>Total Value (in BTC)</CTableDataCell>
                    {tableItems1.map((item, index) => (
                      <CTableDataCell key={index}>{item.totalValue}</CTableDataCell>
                    ))}
                  </CTableRow>
                  <CTableRow>
                    <CTableDataCell>Remaining Quantity (in BTC)</CTableDataCell>
                    {tableItems1.map((item, index) => (
                      <CTableDataCell key={index}>{item.remainingQuantity}</CTableDataCell>
                    ))}
                  </CTableRow>
                  <CTableRow>
                    <CTableDataCell>Sold Today (in BTC)</CTableDataCell>
                    {tableItems1.map((item, index) => (
                      <CTableDataCell key={index}>{item.soldToday}</CTableDataCell>
                    ))}
                  </CTableRow>
                </CTableBody>
              </CTable>
              <br />
              <CTable align="middle" className="mb-0 border" hover responsive>
                <CTableHead color="light">
                  <CTable align="middle" className="mb-0 border" hover responsive>
                    <CTableHead color="light">
                      <CTableRow>
                        <CTableHeaderCell className="text-center">
                          <CIcon icon="cilPeople" />
                        </CTableHeaderCell>
                        <CTableHeaderCell>Top buyers</CTableHeaderCell>
                        <CTableHeaderCell>Monthly purchase</CTableHeaderCell>
                        <CTableHeaderCell className="text-center">
                          Most Bought Product
                        </CTableHeaderCell>
                      </CTableRow>
                    </CTableHead>
                    <CTableBody>
                      {topBuyersData.map((buyer, index) => (
                        <CTableRow key={index}>
                          <CTableDataCell className="text-center">
                            {/* You can display an avatar here */}
                          </CTableDataCell>
                          <CTableDataCell>
                            <div>{buyer.username}</div>
                          </CTableDataCell>
                          <CTableDataCell>
                            <div className="text-medium-emphasis">
                              ${buyer.totalPurchase.toFixed(2)}
                            </div>
                          </CTableDataCell>
                          <CTableDataCell className="text-center">
                            {buyer.mostBoughtProduct}
                          </CTableDataCell>
                        </CTableRow>
                      ))}
                    </CTableBody>
                  </CTable>
                </CTableHead>
              </CTable>
              <br />
              <Purchase />
            </CCardBody>
          </CCard>
        </CCol>
      </CRow>
    </>
  )
}

export default Dashboard
