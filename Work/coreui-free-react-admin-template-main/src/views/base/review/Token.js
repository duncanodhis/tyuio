/* eslint-disable prettier/prettier */
import React, { useState } from 'react'
import {
  CButton,
  CModal,
  CModalHeader,
  CModalTitle,
  CModalBody,
  CModalFooter,
  CFormInput,
  CTooltip,
} from '@coreui/react'

function Token() {
  const [visible, setVisible] = useState(false)
  const [telegramToken, setTelegramToken] = useState('')
  const [tokenSent, setTokenSent] = useState(false)

  // Function to handle sending the token to the endpoint
  const sendTokenToEndpoint = () => {
    // Replace 'YOUR_ENDPOINT_URL' with the actual URL of your endpoint
    const endpointUrl = 'http://127.0.0.1:5000/api/create/disputes_reviews_bot'

    // Make an HTTP request to send the token to the endpoint
    fetch(endpointUrl, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ telegramToken }),
    })
      .then((response) => {
        if (response.ok) {
          setTokenSent(true)
          setVisible(false) // Close the modal upon successful submission
        } else {
          // Handle errors here if needed
          console.error('Failed to send token to the endpoint.')
        }
      })
      .catch((error) => {
        // Handle errors here if needed
        console.error('Error:', error)
      })
  }

  return (
    <>
      <CTooltip
        content="🚀✨🎉 Click this button to add a Telegram token for the Reviews and Disputes bot! 🤖💬🔐"
        placement="right"
      >
        <CButton onClick={() => setVisible(!visible)}>
          Add 🚀 Reviews and Disputes Telegram Bot 🤖
        </CButton>
      </CTooltip>

      <CModal
        visible={visible}
        onClose={() => {
          setVisible(false)
          // Reset tokenSent state when modal is closed
          setTokenSent(false)
        }}
        aria-labelledby="LiveDemoExampleLabel"
      >
        <CModalHeader onClose={() => setVisible(false)}>
          <CModalTitle id="LiveDemoExampleLabel">Enter Reviews and Disputes Token</CModalTitle>
        </CModalHeader>
        <CModalBody>
          <div className="form-group">
            <label htmlFor="telegramToken">Telegram Token:</label>
            <CFormInput
              type="text"
              id="telegramToken"
              value={telegramToken}
              onChange={(e) => setTelegramToken(e.target.value)}
              placeholder="Enter your shop Telegram Token"
            />
          </div>
        </CModalBody>
        <CModalFooter>
          <CButton color="secondary" onClick={() => setVisible(false)}>
            Close
          </CButton>
          <CButton color="primary" onClick={sendTokenToEndpoint} disabled={tokenSent}>
            {tokenSent ? 'Token Sent' : 'Send Token'}
          </CButton>
        </CModalFooter>
      </CModal>
    </>
  )
}

export default Token
