<template>
    <v-container >
        <v-card class="ma-2 pt-1">
        <v-card-title>Statistics</v-card-title>
        <v-simple-table>
            <tbody>
                <tr>
                    <td>Won</td>
                    <td>{{ statistics.won }}</td>
                </tr>
                <tr>
                    <td>Lost</td>
                    <td>{{ statistics.lost }}</td>
                </tr>
                <tr>
                    <td>Total bet</td>
                    <td>{{ statistics.totalBet }}</td>
                </tr>
                <tr>
                    <td>Total bet amount</td>
                    <td>{{ statistics.totalBetAmount }}</td>
                </tr>
                <tr>
                    <td>Effectiveness</td>
                    <td>{{ statistics.effectiveness }}</td>
                </tr>
                <tr>
                    <td>Total win amount</td>
                    <td>{{ statistics.totalWinAmount }}</td>
                </tr>
            </tbody>
        </v-simple-table>
        </v-card>
    </v-container>
</template>

<script>
export default {
  props: {
    statistics: null,
  },
};
</script>