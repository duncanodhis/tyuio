/* eslint-disable prettier/prettier */
// export default Courier;
import React, { useState, useEffect } from 'react';
import axios from 'axios';
import {
  CContainer,
  CNavbar,
  CNavbarNav,
  // CTable,
  // CTableHead,
  // CTableDataCell,
  // CTableRow,
  // CTableHeaderCell,
  // CTableBody,
  CButton,
  // CCollapse,
  // CCard,
  // CCardBody,
  // CModal,
  // CModalHeader,
  // CModalTitle,
  // CModalBody,
  // CModalFooter,
} from '@coreui/react';

import CourierBot from './CourierBot';
import AddCourier from './AddCourier';
import AddTask from './AddTask';
import TaskModal from './TaskModal'

const Courier = () => {
  const [selectedCourier, setSelectedCourier] = useState(null);
  const [showTasksModal, setShowTasksModal] = useState(false);
  const [tasks, setTasks] = useState([]);
  const [couriers, setCouriers] = useState([]);

  console.log(setSelectedCourier,setShowTasksModal,tasks,couriers)
  useEffect(() => {
    fetch('http://127.0.0.1:5000/api/couriers')
      .then((response) => response.json())
      .then((data) => {
        setCouriers(data);
      })
      .catch((error) => console.error('Error fetching couriers:', error));
  }, []);

  useEffect(() => {
    if (showTasksModal && selectedCourier) {
      axios
        .get(`http://127.0.0.1:5000/api/tasks/${selectedCourier.id}`)
        .then((response) => {
          setTasks(response.data);
        })
        .catch((error) => {
          console.error('Error fetching tasks:', error);
        });
    }
  }, [showTasksModal, selectedCourier]);
  return (
    <CContainer>
      <CNavbar expand="md" colorScheme="light" className="bg-light">
        <CNavbarNav>
          <CButton color="primary" shape="rounded-pill">
            <CourierBot />
          </CButton>
          <CButton color="primary" shape="rounded-pill">
            <AddCourier />
          </CButton>
          <CButton color="primary" shape="rounded-pill">
            <AddTask />
          </CButton>
        </CNavbarNav>
      </CNavbar>
      <TaskModal/>
    </CContainer>
  );
};

export default Courier;
