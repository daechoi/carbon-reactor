import { createSlice } from '@reduxjs/toolkit'

const initialState = [
  {
    uid: 1,
    displayName: 'Dae Choi',
    email: 'daechoi@outlook.com',
  },
]

const usersSlice = createSlice({
  name: 'users',
  initialState,
  reducers: {},
})

export default usersSlice.reducer
