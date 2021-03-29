<template>
    <v-container >
        <v-card class="ma-2 pt-1">
        <v-simple-table>
            <tbody>
                <tr>
                    <td>Won</td>
                    <td>{{ statistics.Won }}</td>
                </tr>
                <tr>
                    <td>Lost</td>
                    <td>{{ statistics.Lost }}</td>
                </tr>
                <tr>
                    <td>Total bet</td>
                    <!--<td>{{ statistics. }}</td>-->
                </tr>
                <tr>
                    <td>Total bet amount</td>
                    <td>{{ statistics.totalBetAmount }}</td>
                </tr>
                <tr>
                    <td>Effectiveness</td>
                    <td>{{ statistics.Effectiveness }}</td>
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