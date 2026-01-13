import React from "react";
import AppBar from "@mui/material/AppBar";
import Toolbar from "@mui/material/Toolbar";
import Typography from "@mui/material/Typography";
import IconButton from "@mui/material/IconButton";
import Brightness4Icon from "@mui/icons-material/Brightness4";
import Brightness7Icon from "@mui/icons-material/Brightness7";
import Button from "@mui/material/Button";
import Tooltip from "@mui/material/Tooltip";

interface NavBarProps {
  darkMode: boolean;
  onToggleDarkMode: () => void;
}

const NavBar: React.FC<NavBarProps> = ({ darkMode, onToggleDarkMode }) => {
  return (
    <>
      <AppBar position="static" elevation={0} sx={{ borderBottom: 1, borderColor: 'divider' }}>
        <Toolbar>
          {/* Logo placeholder */}
          <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
            <img
              src="/team-resources-logo.svg"
              alt="Team Resources Logo"
              style={{ height: 40, verticalAlign: "middle", marginRight: 8 }}
            />
          </Typography>
          <Tooltip
            title={darkMode ? "Switch to light mode" : "Switch to dark mode"}
          >
            <IconButton color="inherit" onClick={onToggleDarkMode}>
              {darkMode ? <Brightness7Icon /> : <Brightness4Icon />}
            </IconButton>
          </Tooltip>
          <Tooltip title="Login (future)">
            <Button color="inherit">Login</Button>
          </Tooltip>
        </Toolbar>
      </AppBar>
      {/* Full-width divider below nav */}
      <div style={{ width: '100vw', height: 1, background: 'rgba(0,0,0,0.12)' }} />
    </>
  );
};

export default NavBar;
