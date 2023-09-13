/* eslint-disable prettier/prettier */
/* eslint-disable react/prop-types */
// CourierList.js
import React from 'react';
import { CTable, CTableHead, CTableRow, CTableHeaderCell, CTableBody, CTableDataCell, CButton } from '@coreui/react';

const CourierList = ({ couriers, onViewTasks }) => {
  return (
    <CTable color="light" striped>
      <CTableHead>
        <CTableRow>
          <CTableHeaderCell>Courier Name</CTableHeaderCell>
          <CTableHeaderCell>Tasks</CTableHeaderCell>
        </CTableRow>
      </CTableHead>
      <CTableBody>
        {couriers.map((courier) => (
          <CTableRow key={courier.id}>
            <CTableDataCell>{courier.name}</CTableDataCell>
            <CTableDataCell>
              <CButton color="primary" size="sm" onClick={() => onViewTasks(courier)}>
                View Tasks
              </CButton>
            </CTableDataCell>
          </CTableRow>
        ))}
      </CTableBody>
    </CTable>
  );
};

export default CourierList;
