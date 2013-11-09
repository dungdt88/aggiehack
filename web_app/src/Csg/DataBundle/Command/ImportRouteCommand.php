<?php

namespace Csg\DataBundle\Command;

use Csg\DataBundle\Service\LocationImporter;
use Symfony\Bundle\FrameworkBundle\Command\ContainerAwareCommand;
use Symfony\Component\Console\Input\InputArgument;
use Symfony\Component\Console\Input\InputInterface;
use Symfony\Component\Console\Output\OutputInterface;

class ImportRouteCommand extends ContainerAwareCommand
{
    /**
     * 
     */
    protected function configure()
    {
        $this
            ->setName('data:import-route')
            ->setDescription('Import bus routes from CSV into database')
            ->addArgument(
                'file',
                InputArgument::REQUIRED,
                'Where do you place the CSV file?'
            )
        ;
    }

    /**
     * @param InputInterface $input
     * @param OutputInterface $output
     * @return int|null|void
     */
    protected function execute(InputInterface $input, OutputInterface $output)
    {
        $filePath = $input->getArgument('file');

        if (!file_exists($filePath)) {
            $output->writeln(sprintf("Unable to open file: '%s'", $filePath));
            return;
        }

        /** @var $locationImporter LocationImporter */
        $locationImporter = $this->getContainer()->get('csg_data.service.route_importer');
        $locationImporter->setSource($filePath);

        $output->writeln('Processing data!');
        $locationImporter->process();

        $output->writeln('Import done!');
    }
}
