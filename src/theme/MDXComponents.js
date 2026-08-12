import React from 'react';
import MDXComponents from '@theme-original/MDXComponents';
// Import the Tabs and TabItem components
import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

export default {
  // Re-use the default MDX components
  ...MDXComponents,
  // Overwrite the components you want to make globally available
  Tabs: Tabs,
  TabItem: TabItem,
};
