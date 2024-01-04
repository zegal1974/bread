import React from "react";
import { Layout, Space } from "antd";

const { Header, Footer, Sider, Content } = Layout;

export default class Index extends React.Component {
  render() {
    return (
      <Space
        direction="vertical"
        style={{
          width: "100%",
        }}
        size={[0, 48]}
      >
        <Sider style={siderStyle}>Sider</Sider>
        <Layout>
          <Header style={headerStyle}>Header</Header>
          <Content style={contentStyle}>Content</Content>
          <Footer style={footerStyle}>Footer</Footer>
        </Layout>
      </Space>
    );
  }
}
