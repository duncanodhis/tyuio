import React, { useState } from 'react'
import {
  CButton,
  CModal,
  CModalHeader,
  CModalTitle,
  CModalBody,
  CModalFooter,
  CTooltip,
  CFormInput,
  CToast,
  CToastBody,
  CToastHeader,
} from '@coreui/react'

const CourierBot = () => {
  const [visible, setVisible] = useState(false)
  const [telegramToken, setTelegramToken] = useState('')
  const [showToast, setShowToast] = useState(false)

  const handleAddProduct = () => {
    // Replace 'YOUR_ENDPOINT_URL' with the actual URL of your endpoint
    const endpointUrl = 'http://127.0.0.1:5000/api/create/courier_bot'

    // Make an HTTP request to send the token to the endpoint
    fetch(endpointUrl, {
      method: 'POST', // Use the appropriate HTTP method (POST, GET, etc.)
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ telegramToken }),
    })
      .then((response) => {
        if (response.ok) {
          // Show toast message
          setShowToast(true)

          // Close the modal
          setVisible(false)

          // Reset the token input
          setTelegramToken('')
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
        content="This button creates courier bot ,insert the correct telegram token"
        placement="right"
      >
        <CButton onClick={() => setVisible(!visible)}>Create Courier bot</CButton>
      </CTooltip>

      <CModal alignment="center" visible={visible} onClose={() => setVisible(false)}>
        <CModalHeader>
          <CModalTitle>Create bot</CModalTitle>
        </CModalHeader>
        <CModalBody>
          <CFormInput
            type="text"
            id="telegramToken"
            label="Telegram Token"
            placeholder="Telegram Token"
            text="Must be 8-20 characters long ."
            aria-describedby="exampleFormControlInputHelpInline"
            value={telegramToken}
            onChange={(e) => setTelegramToken(e.target.value)}
          />
        </CModalBody>
        <CModalFooter>
          <CButton color="secondary" onClick={() => setVisible(false)}>
            Close
          </CButton>
          <CTooltip content="This button saves the courier telegram token" placement="right">
            <CButton color="primary" onClick={handleAddProduct}>
              Save changes
            </CButton>
          </CTooltip>
        </CModalFooter>
      </CModal>

      {/* Toast message */}
      <CToast position="top-end">
        <CToast show={showToast} autohide={3000} onDismiss={() => setShowToast(false)}>
          <CToastHeader closeButton>Saved Successfully</CToastHeader>
          <CToastBody>Your changes have been saved successfully.</CToastBody>
        </CToast>
      </CToast>
    </>
  )
}

export default CourierBot
