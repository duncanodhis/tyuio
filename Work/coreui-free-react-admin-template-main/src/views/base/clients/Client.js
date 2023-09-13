/* eslint-disable prettier/prettier */
import React, { useState, useEffect } from 'react';
import {
  CTable,
  CTableHead,
  CTableRow,
  CTableHeaderCell,
  CTableBody,
  CTableDataCell,
  CButton,
  CCollapse,
  CCard,
  CCardBody,
  CHeader,
} from '@coreui/react';
import axios from 'axios';
// import Balance from './Balance';

const Client = () => {
  const [clients, setClients] = useState([]); // State to store clients
  const [selectedClient, setSelectedClient] = useState(null);
  const [visible, setVisible] = useState(false);

  useEffect(() => {
    // Fetch client data when the component mounts
    // Make an HTTP request to your backend API to get the clients data
    // Example using axios:
    axios
      .get('http://127.0.0.1:5000/api/clients')
      .then((response) => {
        setClients(response.data);
      })
      .catch((error) => {
        console.error('Error fetching clients:', error);
      });
  }, []); // Empty dependency array to run this effect only once

  const handleBanClick = (clientId) => {
    // Make an HTTP request to your ban endpoint
    // Example using axios:
    axios
      .post(`/api/ban/${clientId}`)
      .then((response) => {
        // Handle the ban success
      })
      .catch((error) => {
        console.error('Error banning client:', error);
      });

    // For demonstration purposes, you can update the UI directly by removing the banned client from the list
    setClients(clients.filter((client) => client.id !== clientId));
  };

  const handleRowClick = (index) => {
    if (selectedClient === clients[index]) {
      // Clicking the same row again will toggle the collapse
      setVisible(!visible);
    } else {
      // Clicking a different row will select the new client and open the collapse
      setSelectedClient(clients[index]);
      setVisible(true);
    }
  };

  return (
    <>
      <h2>Client Details</h2>
      <CTable>
        <CTableHead>
          <CTableRow>
            <CTableHeaderCell scope="col">Telegram ID</CTableHeaderCell>
            <CTableHeaderCell scope="col">First Name</CTableHeaderCell>
            <CTableHeaderCell scope="col">Last Name</CTableHeaderCell>
            <CTableHeaderCell scope="col">Date Joined</CTableHeaderCell>
            <CTableHeaderCell scope="col">Balance(BTC)</CTableHeaderCell>
            <CTableHeaderCell scope="col">All Time Expenditure</CTableHeaderCell>
            <CTableHeaderCell scope="col">Purchases</CTableHeaderCell>
            <CTableHeaderCell scope="col">Disputes</CTableHeaderCell>
            <CTableHeaderCell scope="col">Reviews</CTableHeaderCell>
          </CTableRow>
        </CTableHead>
        <CTableBody>
          {clients.map((client, index) => (
            <CTableRow
              active
              key={index}
              onClick={() => handleRowClick(index)}
              style={{ cursor: 'pointer' }}
            >
              <CTableDataCell>{client['Telegram ID']}</CTableDataCell>
              <CTableDataCell>{client['First Name']}</CTableDataCell>
              <CTableDataCell>{client['Last Name']}</CTableDataCell>
              <CTableDataCell>{client['Date Joined']}</CTableDataCell>
              <CTableDataCell>{client['Balance']}</CTableDataCell>
              <CTableDataCell>{client['All Time Expenditure']}</CTableDataCell>
              <CTableDataCell>{client['Purchases']}</CTableDataCell>
              <CTableDataCell>{client['Disputes']}</CTableDataCell>
              <CTableDataCell>{client['Reviews']}</CTableDataCell>
              {/* Assuming 'Brought Clients' is a property you want to display */}
              <CTableDataCell>{client['Brought Clients']}</CTableDataCell>
            </CTableRow>
          ))}
        </CTableBody>
      </CTable>
      {selectedClient && (
        <CCollapse visible={visible}>
          <CCard className="mt-3">
            <CCardBody>
              <CHeader className="d-grid gap-2 d-md-flex justify-content-md-center">
                Telegram ID: {selectedClient['Telegram ID']}
              </CHeader>
             
              <div className="d-grid gap-2 d-md-flex justify-content-md-center">
               
                <CButton onClick={() => handleBanClick(selectedClient.id)}>Ban</CButton>
               
              </div>
            
              <div>
                <h5>Client Details:</h5>
                <p>First Name: {selectedClient['First Name']}</p>
                <p>Last Name: {selectedClient['Last Name']}</p>
                <p>Date Joined: {selectedClient['Date Joined']}</p>
                {/* Add more client details as needed */}
              </div>
            </CCardBody>
          </CCard>
        </CCollapse>
      )}
      <div id="toast-container"></div>
    </>
  );
};

export default Client;
