import React from "react";
import Typography from "@mui/material/Typography";
import Box from "@mui/material/Box";

const WelcomeMessage: React.FC = () => (
  <Box sx={{ mt: 4, mb: 2, textAlign: "center" }}>
    <Typography variant="h4" gutterBottom>
      Welcome to AgentSpace
    </Typography>
    <Typography variant="body1">
      Start by selecting a request and providing context to generate the asset you are seeking.
    </Typography>
  </Box>
);

export default WelcomeMessage;
