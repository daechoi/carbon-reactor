import { NavLink } from 'react-router-dom'

export const Navbar: React.FC = () => {
  return (
    <nav className="nav-wrapper blue darken-4 px1">
      <div>
        <NavLink to="/" className="brand-logo">
          Carbon Reactor
        </NavLink>
        <ul className="right hide-on-med-and-down">
          <li cy-data="home-nav-link">
            <NavLink to="/">Home</NavLink>
          </li>
          <li>
            <NavLink to="/about">About</NavLink>
          </li>
        </ul>
      </div>
    </nav>
  )
}
