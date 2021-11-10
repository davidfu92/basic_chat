import React from 'react';
import { withStyles } from '@material-ui/core/styles';
import SwipeableViews from 'react-swipeable-views';
import Tabs from '@material-ui/core/Tabs';
import Tab from '@material-ui/core/Tab';
import Grid from '@material-ui/core/Grid';

import APIClient from '../apiClient'

const styles = theme => ({
  root: {
    flexGrow: 1,
    marginTop: 30
  },
  paper: {
    padding: theme.spacing(2),
    textAlign: 'center',
    color: theme.palette.text.secondary,
  },
});

class Home extends React.Component {
  state = {
    value: 0,
    users: [],
    msgs: []
  };

  componentDidMount() {
    const accessToken = this.props.authState.accessToken.accessToken;
    this.apiClient = new APIClient(accessToken);
    this.apiClient.getMessage().then((data) =>
      this.setState({...this.state, msgs: data})
    );
  }

  handleTabChange = (event, value) => {
    this.setState({ value });
  };

  handleTabChangeIndex = index => {
    this.setState({ value: index });
  };

  resetRepos = messages => this.setState({ ...this.state, messages })

  isMessage = msg => this.state.msg.find(r => r.id === msg.id)
    onMessage = (msg) => {
      this.updateBackend(msg);
  }

  updateBackend = (msg) => {
    if (this.isMessage(msg)) {
      this.apiClient.deleteMessage(msg);
    } else {
      this.apiClient.createMessage(msg);
    }
    this.updateState(msg);
  }

  updateState = (msg) => {
    if (this.isMessage(msg)) {
      this.setState({
        ...this.state,
        kudos: this.state.msgs.filter( r => r.id !== msg.id )
      })
    } else {
      this.setState({
        ...this.state,
        kudos: [msg, ...this.state.msgs]
      })
    }
  }

  render() {
    return (
      <div className={styles.root}>
        <Tabs
          value={this.state.value}
          onChange={this.handleTabChange}
          indicatorColor="primary"
          textColor="primary"
          variant="fullWidth"
        >
          <Tab label="Message" />
          <Tab label="Search" />
        </Tabs>
      
        <SwipeableViews
          axis={'x-reverse'}
          index={this.state.value}
          onChangeIndex={this.handleTabChangeIndex}
        >
          <Grid container spacing={10} style={{padding: '20px 0'}}>
            { this.renderRepos(this.state.kudos) }
          </Grid>
          <Grid container spacing={10} style={{padding: '20px 0'}}>
            { this.renderRepos(this.state.messages) }
          </Grid>
        </SwipeableViews>
      </div>
    );
  }
}

msgrtWebVitals();

export default Home;
