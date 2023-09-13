/* eslint-disable prettier/prettier */
import React, { useState, useEffect } from 'react'
import { CButton, CCollapse, CCard, CCardBody } from '@coreui/react'

function Dispute() {
  const [visible, setVisible] = useState(false)
  const [data, setData] = useState([])

  // Function to fetch data from your endpoint (replace 'yourEndpoint' with the actual endpoint URL)
  const fetchData = async () => {
    try {
      const response = await fetch('http://127.0.0.1:5000/api/disputes')
      const result = await response.json()
      setData(result) // Assuming your data is an array
    } catch (error) {
      console.error('Error fetching data:', error)
    }
  }

  useEffect(() => {
    fetchData() // Fetch data when the component mounts
  }, [])

  return (
    <>
      {data.map((item, index) => (
        <div key={index}>
          <CButton color="primary" onClick={() => setVisible(!visible)} className="mb-2">
            View Details for Dispute {index + 1}
          </CButton>
          <CCollapse visible={visible}>
            <CCard className="mt-3">
              <CCardBody>
                <p>
                  <strong>Telegram ID:</strong> {item.user_id}
                </p>
                <p>
                  <strong>Order ID:</strong> {item.order_id}
                </p>
                <p>
                  <strong>Urgency Number:</strong> {item.urgency}
                </p>
                <p>
                  <strong>Comment:</strong> {item.message}
                </p>
                <p>
                  <strong>Created at:</strong> {item.created_at}
                </p>
              </CCardBody>
            </CCard>
          </CCollapse>
        </div>
      ))}
    </>
  )
}

export default Dispute
