/* eslint-disable prettier/prettier */
import React, { useState } from 'react';
import axios from 'axios';
import {
  CButton,
  CModal,
  CModalHeader,
  CModalTitle,
  CModalBody,
  CModalFooter,
  CTooltip,
  CForm,
  CCol,
  CFormInput,
  CToast,
  CToastBody,
  CToastHeader,
} from '@coreui/react';

const AddCourier = () => {
  const [visible, setVisible] = useState(false);
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [showToast, setShowToast] = useState(false);

  const handleCourier = async () => {
    try {
      const courierData = {
        username: username,
        password: password,
      };
      console.log(courierData)
      // Call the API to create the courier
      const response = await axios.post('http://127.0.0.1:5000/api/couriers', courierData, {
        headers: {
          'Content-Type': 'application/json',
        },
      });

      console.log('Courier data submitted successfully:', response.data);

      // Show toast message
      setShowToast(true);

      // Close the modal
      setVisible(false);
    } catch (error) {
      // Handle any errors that occurred during the API call
      console.error('Error submitting courier data:', error);
    }
  };

  return (
    <>
      <CTooltip
        content="Make sure to create 🌱packaging,📌Addresses on the navigation bar 👆 first before adding product"
        placement="right"
      >
        <CButton onClick={() => setVisible(!visible)}>Create Courier</CButton>
      </CTooltip>

      <CModal alignment="center" visible={visible} onClose={() => setVisible(false)}>
        <CModalHeader>
          <CModalTitle>Create Courier</CModalTitle>
        </CModalHeader>
        <CModalBody>
          <CForm className="row g-3">
            <CCol md={6}>
              <CFormInput
                id="username"
                label="username"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
              />
            </CCol>
            <CCol md={6}>
              <CFormInput
                id="password"
                label="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
              />
            </CCol>
          </CForm>
        </CModalBody>
        <CModalFooter>
          <CButton color="secondary" onClick={() => setVisible(false)}>
            Close
          </CButton>
          <CTooltip
            content="Stock price is the same as package price, so you have to input the selling price for the clients to see"
            placement="right"
          >
            <CButton color="primary" onClick={handleCourier}>
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
  );
};

export default AddCourier;
