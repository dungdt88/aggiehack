<?php

namespace Csg\DataBundle\Command;

use Csg\DataBundle\Service\DistanceCalculator;
use Symfony\Bundle\FrameworkBundle\Command\ContainerAwareCommand;
use Symfony\Component\Console\Input\InputArgument;
use Symfony\Component\Console\Input\InputInterface;
use Symfony\Component\Console\Output\OutputInterface;

class CalculateDistanceCommand extends ContainerAwareCommand
{
    /**
     *
     */
    protected function configure()
    {
        $this
            ->setName('data:calculate-distances')
        ;
    }

    /**
     * @param InputInterface $input
     * @param OutputInterface $output
     * @return int|null|void
     */
    protected function execute(InputInterface $input, OutputInterface $output)
    {
        /** @var $distanceCalculator DistanceCalculator */
        $distanceCalculator = $this->getContainer()->get('csg_data.service.distance_calculator');
        $distanceCalculator->calculateDistance();

        $output->writeln('Done!');
    }
}
