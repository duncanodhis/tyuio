/* eslint-disable prettier/prettier */
import React, { useState, useEffect } from 'react'
import axios from 'axios'
import { CButton, CCard, CCardBody, CCollapse, CCol, CRow } from '@coreui/react'

const Purchase = () => {
  const [visibleTopProduct, setVisibleTopProduct] = useState(false)
  const [visibleLatestPurchase, setVisibleLatestPurchase] = useState(false)
  const [topProductData, setTopProductData] = useState({})
  const [latestPurchaseData, setLatestPurchaseData] = useState({})

  // Fetch top product of the day data
  const fetchTopProductData = async () => {
    try {
      const response = await axios.get('http://127.0.0.1:5000/api/top-product-day')
      setTopProductData(response.data)
    } catch (error) {
      console.error('Error fetching top product data:', error)
    }
  }

  // Fetch latest purchase data
  const fetchLatestPurchaseData = async () => {
    try {
      const response = await axios.get('http://127.0.0.1:5000/api/latest-purchase')
      setLatestPurchaseData(response.data)
    } catch (error) {
      console.error('Error fetching latest purchase data:', error)
    }
  }

  useEffect(() => {
    fetchTopProductData()
    fetchLatestPurchaseData()
  }, [])

  return (
    <div className="mt-4">
      <CRow className="mb-3">
        <CCol xs="auto">
          <CButton onClick={() => setVisibleTopProduct(!visibleTopProduct)}>Top Product</CButton>
        </CCol>
        <CCol xs="auto">
          <CButton onClick={() => setVisibleLatestPurchase(!visibleLatestPurchase)}>
            Latest Purchase
          </CButton>
        </CCol>
      </CRow>
      <CRow>
        <CCol xs={6}>
          <CCollapse visible={visibleTopProduct}>
            <CCard className="mb-3">
              <CCardBody>
                <h3>Top Product of the Day</h3>
                <p>Product: {topProductData.product}</p>
                <p>Sales: {topProductData.sales}</p>
              </CCardBody>
            </CCard>
          </CCollapse>
        </CCol>
        <CCol xs={6}>
          <CCollapse visible={visibleLatestPurchase}>
            <CCard className="mb-3">
              <CCardBody>
                <h3>Latest Purchase</h3>
                <p>Product: {latestPurchaseData.product?.name}</p>
                <p>Buyer: {latestPurchaseData.buyer?.username}</p>
                <p>Product price($): {latestPurchaseData.product?.package_price}</p>

              </CCardBody>
            </CCard>
          </CCollapse>
        </CCol>
      </CRow>
    </div>
  )
}

export default Purchase
