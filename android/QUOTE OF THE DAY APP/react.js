import React, { useEffect, useState } from 'react';
import { View, Text, Button, Share, StyleSheet } from 'react-native';

const HomeScreen = () => {
  const [quote, setQuote] = useState({ text: '', author: '' });

  const fetchQuote = async () => {
    // Fetch a random quote from an API or local list
    const response = await fetch('https://api.quotable.io/random');
    const data = await response.json();
    setQuote({ text: data.content, author: data.author });
  };

  useEffect(() => {
    fetchQuote();
  }, []);

  const shareQuote = async () => {
    try {
      await Share.share({
        message: `${quote.text} - ${quote.author}`,
      });
    } catch (error) {
      console.log(error.message);
    }
  };

  return (
    <View style={styles.container}>
      <Text style={styles.quote}>{quote.text}</Text>
      <Text style={styles.author}>- {quote.author}</Text>
      <Button title="Share" onPress={shareQuote} />
      <Button title="Refresh" onPress={fetchQuote} />
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    padding: 20,
  },
  quote: {
    fontSize: 24,
    textAlign: 'center',
    marginBottom: 20,
  },
  author: {
    fontSize: 18,
    textAlign: 'center',
    marginBottom: 20,
  },
});

export default HomeScreen;