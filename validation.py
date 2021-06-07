import csv

targets = [1, 5, 10]
supersenses = [2, 3, 6, 7, 11, 12]
scene_roles = [2, 6, 11]
snacs = ('??', '`d', '`i', 'Agent', 'Ancillary', 'Beneficiary', 'Causer', 'Characteristic', 'Circumstance',
         'ComparisonRef', 'Cost', 'Direction', 'Duration', 'EndTime', 'Experiencer', 'Explanation',
         'Extent', 'Focus', 'Frequency', 'Gestalt', 'Goal', 'Identity', 'Instrument', 'Interval', 'Locus',
         'Manner', 'Means', 'NONSNACS', 'Org', 'OrgMember', 'Originator', 'PartPortion', 'Path', 'Possession',
         'Possessor', 'Purpose', 'QuantityItem', 'QuantityValue', 'Recipient', 'SocialRel', 'Source',
         'StartTime', 'Stimulus', 'Stuff', 'Theme', 'Time', 'Topic', 'Whole', '', 'Temporal', 'Species',
         'RateUnit', 'Approximator', 'Ensemble', '`$')

def main():
    for i in range(1, 28):
        with open(f'annotations/lp_adjudicated_cleaned/{i}.csv', 'r') as fin:
            reader = csv.reader(fin)
            for line, row in enumerate(reader):
                if line == 0: continue

                try:
                    for x in targets:
                        assert row[x].strip() == row[x], f'Target {row[x]} should not have trailing/leading whitespace.'
                        assert row[x] != 'की', f'Target {row[x]} should be lemmatised.'
                        assert row[x] != 'के', f'Target {row[x]} should be lemmatised.' 
                        assert row[x] != 'सी', f'Target {row[x]} should be lemmatised.'

                    for x in supersenses:
                        assert row[x].strip() == row[x], f'Supersense "{row[x]}" should not have trailing/leading whitespace.'
                        assert row[x] in snacs, f'Supersense "{row[x]}" should be part of the SNACS hierarchy.'

                    for x in scene_roles:
                        if row[x]:
                            assert row[x + 1], 'Target with scene role should have function annotation.'
                        if row[x + 1]:
                            assert row[x], 'Target with function should have scene role annotation.'

                    if row[2]:
                        assert row[1], 'Labelled target should have lemmatised adposition given.'
                    
                except Exception as e:
                    print(i, line)
                    print(row)
                    print(e)
                    input()
                    continue

if __name__ == '__main__':
    main()