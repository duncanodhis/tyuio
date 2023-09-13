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
  CModal,
  CModalBody,
  CModalHeader,
  CModalTitle,
} from '@coreui/react'

import { CChartLine } from '@coreui/react-chartjs'
import CIcon from '@coreui/icons-react'
import {
  cibCcAmex,
  cibCcApplePay,
  cibCcMastercard,
  cibCcPaypal,
  cibCcStripe,
  cibCcVisa,
  cifBr,
  cifEs,
  cifFr,
  cifIn,
  cifPl,
  cifUs,
  cilPeople,
} from '@coreui/icons'

import avatar1 from 'src/assets/images/avatars/1.jpg'
import avatar2 from 'src/assets/images/avatars/2.jpg'
import avatar3 from 'src/assets/images/avatars/3.jpg'
import avatar4 from 'src/assets/images/avatars/4.jpg'
import avatar5 from 'src/assets/images/avatars/5.jpg'
import avatar6 from 'src/assets/images/avatars/6.jpg'

import WidgetsDropdown from '../widgets/WidgetsDropdown'

const Dashboard = () => {
  const [showAccountModal, setShowAccountModal] = useState(false)
  const [showPurchaseModal, setShowPurchaseModal] = useState(false)
  const [showCommentsModal, setShowCommentsModal] = useState(false)
  const [showStatisticsModal, setShowStatisticsModal] = useState(false)
  const [salesData, setSalesData] = useState({ labels: [], datasets: [] })
  const [selectedPeriod, setSelectedPeriod] = useState('Month')
  const [tableItems, setTableItems] = useState([])

  const [metrics, setMetrics] = useState({
    sales: 0,
    earnings: 0,
    profitMargin: 0,
    avgOrderValue: 0,
    customerLifetime: 0,
  })
  const [clientsData, setClientsData] = useState({
    newClients: 0,
    recurringClients: 0,
    progressGroupMetrics: [],
  })
  const fetchSalesMetricsData = async () => {
    try {
      const earningsResponse = await axios.get('http://127.0.0.1:5000/api/earnings') // Update with actual endpoint
      const salesResponse = await axios.get('http://127.0.0.1:5000/api/sales') // Update with actual endpoint
      const clientsResponse = await axios.get('http://127.0.0.1:5000/api/clients') // Update with actual endpoint
      const goodsResponse = await axios.get('http://127.0.0.1:5000/api/goods') // Update with actual endpoint

      const earningsData = earningsResponse.data
      const salesData = salesResponse.data
      const clientsData = clientsResponse.data
      const goodsData = goodsResponse.data
      const processedTableItems = earningsData.map((earningsItem, index) => ({
        period: earningsItem.period,
        earnings: earningsItem.earnings,
        sales: salesData[index].sales,
        clients: clientsData[index].clients,
        goods: goodsData[index].goods,
      }))
      // Process data and create table items based on periods
      setTableItems(processedTableItems)
    } catch (error) {
      console.error('Error fetching metrics data:', error)
    }
  }
  useEffect(() => {
    fetchSalesMetricsData()
  }, [])

  const fetchClientsData = async () => {
    try {
      const clientsResponse = await axios.get('http://127.0.0.1:5000/api/weekly-clients') // Update with actual endpoint
      const clientsData = clientsResponse.data

      setClientsData(clientsData)
    } catch (error) {
      console.error('Error fetching clients data:', error)
    }
  }

  useEffect(() => {
    fetchClientsData()
  }, [])
  const toggleAccountModal = () => {
    setShowAccountModal(!showAccountModal)
  }

  const togglePurchaseModal = () => {
    setShowPurchaseModal(!showPurchaseModal)
  }

  const toggleCommentsModal = () => {
    setShowCommentsModal(!showCommentsModal)
  }

  const toggleStatisticsModal = () => {
    setShowStatisticsModal(!showStatisticsModal)
  }

  const handlePeriodChange = (period) => {
    setSelectedPeriod(period)
  }

  const fetchData = async () => {
    try {
      const response = await axios.get('http://127.0.0.1:5000/api/orders')
      const orders = response.data

      // Process orders data to group by product and time period
      const productDataMap = new Map() // Map to store product data

      orders.forEach((order) => {
        const createdAtDate = new Date(order.created_at)
        const month = createdAtDate.getMonth() // Assuming orders are within the same year

        // Initialize product data entry if not exists
        if (!productDataMap.has(order.product_id)) {
          productDataMap.set(order.product_id, {
            label: `Product ${order.product_id}`, // Update with actual product name
            backgroundColor: `rgba(0, 123, 255, 0.1)`,
            borderColor: `rgba(0, 123, 255, 1)`,
            borderWidth: 2,
            data: Array(12).fill(0), // Initialize data for each month
            fill: true,
          })
        }

        // Increment data value for the corresponding month
        const productData = productDataMap.get(order.product_id)
        productData.data[month] += order.total_price // Assuming total_price represents sales value
      })

      const processedData = {
        labels: [
          'January',
          'February',
          'March',
          'April',
          'May',
          'June',
          'July',
          'August',
          'September',
          'October',
          'November',
          'December',
        ],
        datasets: Array.from(productDataMap.values()), // Convert Map values to an array
      }

      setSalesData(processedData)
    } catch (error) {
      console.error('Error fetching data:', error)
    }
  }

  useEffect(() => {
    fetchData()
  }, [])

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

  const tableExample = [
    {
      avatar: { src: avatar1, status: 'success' },
      user: {
        name: 'Yiorgos Avraamu',
        new: true,
        registered: 'Jan 1, 2021',
      },
      country: { name: 'USA', flag: cifUs },
      usage: {
        value: 50,
        period: 'Jun 11, 2021 - Jul 10, 2021',
        color: 'success',
      },
      payment: { name: 'Mastercard', icon: cibCcMastercard },
      activity: '10 sec ago',
    },
    {
      avatar: { src: avatar2, status: 'danger' },
      user: {
        name: 'Avram Tarasios',
        new: false,
        registered: 'Jan 1, 2021',
      },
      country: { name: 'Brazil', flag: cifBr },
      usage: {
        value: 22,
        period: 'Jun 11, 2021 - Jul 10, 2021',
        color: 'info',
      },
      payment: { name: 'Visa', icon: cibCcVisa },
      activity: '5 minutes ago',
    },
    {
      avatar: { src: avatar3, status: 'warning' },
      user: { name: 'Quintin Ed', new: true, registered: 'Jan 1, 2021' },
      country: { name: 'India', flag: cifIn },
      usage: {
        value: 74,
        period: 'Jun 11, 2021 - Jul 10, 2021',
        color: 'warning',
      },
      payment: { name: 'Stripe', icon: cibCcStripe },
      activity: '1 hour ago',
    },
    {
      avatar: { src: avatar4, status: 'secondary' },
      user: { name: 'Enéas Kwadwo', new: true, registered: 'Jan 1, 2021' },
      country: { name: 'France', flag: cifFr },
      usage: {
        value: 98,
        period: 'Jun 11, 2021 - Jul 10, 2021',
        color: 'danger',
      },
      payment: { name: 'PayPal', icon: cibCcPaypal },
      activity: 'Last month',
    },
    {
      avatar: { src: avatar5, status: 'success' },
      user: {
        name: 'Agapetus Tadeáš',
        new: true,
        registered: 'Jan 1, 2021',
      },
      country: { name: 'Spain', flag: cifEs },
      usage: {
        value: 22,
        period: 'Jun 11, 2021 - Jul 10, 2021',
        color: 'primary',
      },
      payment: { name: 'Google Wallet', icon: cibCcApplePay },
      activity: 'Last week',
    },
    {
      avatar: { src: avatar6, status: 'danger' },
      user: {
        name: 'Friderik Dávid',
        new: true,
        registered: 'Jan 1, 2021',
      },
      country: { name: 'Poland', flag: cifPl },
      usage: {
        value: 43,
        period: 'Jun 11, 2021 - Jul 10, 2021',
        color: 'success',
      },
      payment: { name: 'Amex', icon: cibCcAmex },
      activity: 'Last week',
    },
  ]
  const metricsDisplayItems = [
    { title: 'Total Sales', value: metrics.sales, color: 'info' },
    { title: 'Total Earnings', value: metrics.earnings, color: 'success' },
    { title: 'Profit Margin', value: metrics.profitMargin, color: 'warning' },
    { title: 'Average Order Value', value: metrics.avgOrderValue, color: 'primary' },
    { title: 'Customer Lifetime Value', value: metrics.customerLifetime, color: 'danger' },
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
              <CRow>
                <CCol xs={12} md={6} xl={6}>
                  <CRow>
                    <CCol sm={6}>
                      <div className="border-start border-start-4 border-start-info py-1 px-3">
                        <div className="text-medium-emphasis small">New Clients</div>
                        <div className="fs-5 fw-semibold">{clientsData.newClients}</div>
                      </div>
                    </CCol>
                    <CCol sm={6}>
                      <div className="border-start border-start-4 border-start-danger py-1 px-3 mb-3">
                        <div className="text-medium-emphasis small">Recurring Clients</div>
                        <div className="fs-5 fw-semibold">{clientsData.recurringClients}</div>
                      </div>
                    </CCol>
                  </CRow>
                  <hr className="mt-0" />
                  {clientsData.progressGroupMetrics.map((item, index) => (
                    <div className="progress-group mb-4" key={index}>
                      <div className="progress-group-prepend">
                        <span className="text-medium-emphasis small">{item.dayOfWeek}</span>
                      </div>
                      <div className="progress-group-bars">
                        <CProgress thin color="info" value={item.newClients} />
                        <CProgress thin color="danger" value={item.recurringClients} />
                      </div>
                      <div className="progress-group-labels">
                        <span className="text-info">{item.newClients}</span>
                        <span className="text-danger">{item.recurringClients}</span>
                      </div>
                    </div>
                  ))}
                </CCol>
              </CRow>
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
                    <CTableHeaderCell>Goods</CTableHeaderCell>
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
                      <CTableDataCell>{item.goods}</CTableDataCell>
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
                      <strong>Summary(in $)</strong>
                    </CTableDataCell>
                    <CTableDataCell>Total Value(in $)</CTableDataCell>
                    {tableItems1.map((item, index) => (
                      <CTableDataCell key={index}>{item.totalValue}</CTableDataCell>
                    ))}
                  </CTableRow>
                  <CTableRow>
                    <CTableDataCell>Remaining Quantity(in $)</CTableDataCell>
                    {tableItems1.map((item, index) => (
                      <CTableDataCell key={index}>{item.remainingQuantity}</CTableDataCell>
                    ))}
                  </CTableRow>
                  <CTableRow>
                    <CTableDataCell>Sold Today(in $)</CTableDataCell>
                    {tableItems1.map((item, index) => (
                      <CTableDataCell key={index}>{item.soldToday}</CTableDataCell>
                    ))}
                  </CTableRow>
                </CTableBody>
              </CTable>
              <br />
              <CTable align="middle" className="mb-0 border" hover responsive>
                <CTableHead color="light">
                  <CTableRow>
                    <CTableHeaderCell className="text-center">
                      <CIcon icon={cilPeople} />
                    </CTableHeaderCell>
                    <CTableHeaderCell> Top buyers</CTableHeaderCell>
                    <CTableHeaderCell className>City</CTableHeaderCell>
                    <CTableHeaderCell className>Location</CTableHeaderCell>
                    <CTableHeaderCell>Monthly purchase</CTableHeaderCell>
                    <CTableHeaderCell className="text-center">Today purchase</CTableHeaderCell>
                    <CTableHeaderCell>Activity</CTableHeaderCell>
                  </CTableRow>
                </CTableHead>
                <CTableBody>
                  {tableExample.map((item, index) => (
                    <CTableRow v-for="item in tableItems" key={index}>
                      <CTableDataCell className="text-center">
                        <CAvatar size="md" src={item.avatar.src} status={item.avatar.status} />
                      </CTableDataCell>
                      <CTableDataCell>
                        <div>{item.user.name}</div>
                        <div className="small text-medium-emphasis">
                          <span>{item.user.new ? 'New' : 'Recurring'}</span> | Registered:{' '}
                          {item.user.registered}
                        </div>
                      </CTableDataCell>
                      <CTableDataCell className="text-center">
                        <CIcon size="xl" icon={item.country.flag} title={item.country.name} />
                      </CTableDataCell>
                      <CTableDataCell className="text-center">
                        <CIcon size="xl" icon={item.country.flag} title={item.country.name} />
                      </CTableDataCell>
                      <CTableDataCell>
                        <div className="clearfix">
                          <div className="float-start">
                            <strong>{item.usage.value}%</strong>
                          </div>
                          <div className="float-end">
                            <small className="text-medium-emphasis">{item.usage.period}</small>
                          </div>
                        </div>
                        <CProgress thin color={item.usage.color} value={item.usage.value} />
                      </CTableDataCell>
                      <CTableDataCell className="text-center">
                        <CIcon size="xl" icon={item.payment.icon} />
                      </CTableDataCell>
                      <CTableDataCell>
                        <div className="small text-medium-emphasis">Last login</div>
                        <strong>{item.activity}</strong>
                      </CTableDataCell>
                    </CTableRow>
                  ))}
                </CTableBody>
              </CTable>
              <br />
              <CTable align="middle" className="mb-0 border" hover responsive>
                <CTableBody>
                  <CTableRow>
                    <CTableDataCell>
                      <CButton color="primary" onClick={toggleAccountModal}>
                        Top product of the day
                      </CButton>
                    </CTableDataCell>
                    <CTableDataCell>
                      <CButton color="primary" onClick={toggleAccountModal}>
                        Account Replenishment
                      </CButton>
                    </CTableDataCell>
                    <CTableDataCell>
                      <CButton color="primary" onClick={togglePurchaseModal}>
                        Latest Purchase
                      </CButton>
                    </CTableDataCell>
                  </CTableRow>
                  <CTableRow>
                    <CTableDataCell>
                      <CButton color="primary" onClick={toggleCommentsModal}>
                        Comments
                      </CButton>
                    </CTableDataCell>
                    <CTableDataCell>
                      <CButton color="primary" onClick={toggleStatisticsModal}>
                        Statistics by City
                      </CButton>
                    </CTableDataCell>
                    <CTableDataCell>
                      <CButton color="primary" onClick={toggleStatisticsModal}>
                        Click Me here
                      </CButton>
                    </CTableDataCell>
                  </CTableRow>
                </CTableBody>

                <CModal show={showAccountModal} onClose={toggleAccountModal}>
                  <CModalHeader closeButton>
                    <CModalTitle>Account Replenishment</CModalTitle>
                  </CModalHeader>
                  <CModalBody>{/* Content for the Account Replenishment pop-up */}</CModalBody>
                </CModal>

                <CModal show={showPurchaseModal} onClose={togglePurchaseModal}>
                  <CModalHeader closeButton>
                    <CModalTitle>Latest Purchase</CModalTitle>
                  </CModalHeader>
                  <CModalBody>{/* Content for the Latest Purchase pop-up */}</CModalBody>
                </CModal>

                <CModal show={showCommentsModal} onClose={toggleCommentsModal}>
                  <CModalHeader closeButton>
                    <CModalTitle>Comments</CModalTitle>
                  </CModalHeader>
                  <CModalBody>{/* Content for the Comments pop-up */}</CModalBody>
                </CModal>

                <CModal show={showStatisticsModal} onClose={toggleStatisticsModal}>
                  <CModalHeader closeButton>
                    <CModalTitle>Statistics by City</CModalTitle>
                  </CModalHeader>
                  <CModalBody>{/* Content for the Statistics by City pop-up */}</CModalBody>
                </CModal>
              </CTable>
            </CCardBody>
          </CCard>
        </CCol>
      </CRow>
    </>
  )
}

export default Dashboard
